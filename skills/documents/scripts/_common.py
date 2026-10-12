"""Shared helpers for the documents skill scripts (standard library only)."""
import os
import shutil
import stat
import sys
import zipfile
from xml.etree import ElementTree as ET

# Limits for untrusted Office/PDF packages.
MAX_PART_BYTES = 64 * 1024 * 1024        # one XML part, uncompressed
MAX_TOTAL_BYTES = 512 * 1024 * 1024      # whole package, uncompressed
MAX_RATIO = 200                          # uncompressed / compressed, per part


class PackageError(Exception):
    """The file is not a usable, safe Office Open XML package."""


def open_package(path):
    """Open an OOXML file as a ZipFile after cheap zip-bomb checks."""
    if not os.path.isfile(path):
        raise PackageError(f"not a file: {path}")
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile as e:
        raise PackageError(f"not a zip/OOXML package ({e}); legacy .doc/.xls/.ppt must be converted first")
    total = 0
    for info in z.infolist():
        total += info.file_size
        if info.file_size > MAX_PART_BYTES:
            raise PackageError(f"part too large: {info.filename}")
        if info.compress_size and info.file_size / info.compress_size > MAX_RATIO and info.file_size > 1_000_000:
            raise PackageError(f"suspicious compression ratio: {info.filename}")
    if total > MAX_TOTAL_BYTES:
        raise PackageError("package too large when uncompressed")
    return z


def read_xml(z, name):
    """Parse one XML part. Refuses entity declarations (entity-expansion bombs, XXE)."""
    try:
        data = z.read(name)
    except KeyError:
        return None
    if b"<!ENTITY" in data:
        raise PackageError(f"refusing XML with entity declarations: {name}")
    return ET.fromstring(data)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def find_soffice():
    """Locate LibreOffice's command-line binary, or None."""
    env = os.environ.get("SOFFICE")
    if env and os.path.exists(env):
        return env
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    for p in (
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/lib/libreoffice/program/soffice",
        "/opt/libreoffice/program/soffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ):
        if os.path.exists(p):
            return p
    return None


def safe_extract(z, dest, force=False):
    """Extract a package, rejecting path traversal, absolute paths and symlinks."""
    dest = os.path.abspath(dest)
    if os.path.exists(dest) and os.listdir(dest) and not force:
        raise PackageError(f"destination not empty: {dest} (use --force)")
    os.makedirs(dest, exist_ok=True)
    for info in z.infolist():
        name = info.filename
        if name.startswith(("/", "\\")) or ".." in name.replace("\\", "/").split("/") or ":" in name.split("/")[0]:
            raise PackageError(f"unsafe path in package: {name}")
        mode = info.external_attr >> 16
        if stat.S_ISLNK(mode):
            raise PackageError(f"symlink entry in package: {name}")
        target = os.path.abspath(os.path.join(dest, name))
        if not target.startswith(dest + os.sep):
            raise PackageError(f"unsafe path in package: {name}")
        if info.is_dir():
            os.makedirs(target, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with z.open(info) as src, open(target, "wb") as out:
            shutil.copyfileobj(src, out)
    return dest


def die(msg, code=2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def clean_err(proc, limit=300):
    """Subprocess error text without LibreOffice's harmless Fontconfig chatter."""
    text = (proc.stderr or "") + "\n" + (proc.stdout or "")
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("Fontconfig")]
    return " ".join(lines)[:limit] or "no error output"
