#!/usr/bin/env python3
"""Inventory GLB/glTF without dependencies or network access; not a spec validator."""

import argparse
import json
import struct
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def integer(value, label):
    if type(value) is not int or value < 0:
        raise ValueError("{} must be a nonnegative integer".format(label))
    return value


def item(items, index, label):
    index = integer(index, label)
    if index >= len(items):
        raise ValueError("{} references a missing element".format(label))
    return items[index]


def read_document(path):
    raw = path.read_bytes()
    chunks = []
    binary_size = None
    if raw[:4] == b"glTF":
        if len(raw) < 12:
            raise ValueError("Truncated GLB header")
        _, version, declared_size = struct.unpack_from("<4sII", raw)
        if version != 2 or declared_size != len(raw):
            raise ValueError("GLB version or declared file length is invalid")
        offset = 12
        json_data = None
        while offset < len(raw):
            if offset + 8 > len(raw):
                raise ValueError("Truncated GLB chunk header")
            size, kind = struct.unpack_from("<II", raw, offset)
            offset += 8
            if size % 4 or offset + size > len(raw):
                raise ValueError("Invalid GLB chunk length or alignment")
            if not chunks and kind != 0x4E4F534A:
                raise ValueError("First GLB chunk must be JSON")
            if kind == 0x4E4F534A:
                if json_data is not None:
                    raise ValueError("Duplicate GLB JSON chunk")
                json_data = raw[offset:offset + size]
            elif kind == 0x004E4942:
                if binary_size is not None or len(chunks) != 1:
                    raise ValueError("Invalid position or duplication of GLB BIN chunk")
                binary_size = size
            chunks.append({"type": hex(kind), "bytes": size})
            offset += size
        if json_data is None:
            raise ValueError("Missing GLB JSON chunk")
        doc = json.loads(json_data)
        container = "GLB"
    else:
        if path.suffix.lower() != ".gltf":
            raise ValueError("Expected a GLB file or a .gltf JSON file")
        doc = json.loads(raw.decode("utf-8-sig"))
        container = "glTF JSON"
    if not isinstance(doc, dict) or doc.get("asset", {}).get("version") != "2.0":
        raise ValueError("Expected a glTF 2.0 document")
    return doc, container, len(raw), chunks, binary_size


def resource_status(uri, directory):
    """Never fetch remote resources or print URI queries, credentials, or data blobs."""
    if not isinstance(uri, str):
        raise ValueError("Resource URI must be a string")
    parts = urlsplit(uri)
    if parts.scheme == "data":
        return {"storage": "data-uri", "contents_checked": False}
    if parts.scheme or parts.netloc:
        return {"storage": "external-uri", "scheme": parts.scheme or "relative-network",
                "host": parts.hostname, "contents_checked": False}
    if parts.query or parts.fragment:
        return {"storage": "uri-with-query-or-fragment", "contents_checked": False}
    relative = Path(unquote(parts.path))
    target = (directory / relative).resolve()
    try:
        local = target.relative_to(directory)
    except ValueError:
        return {"storage": "outside-asset-directory", "contents_checked": False}
    exists = target.is_file()
    return {"storage": "local-file", "path": local.as_posix(), "exists": exists,
            "bytes": target.stat().st_size if exists else None, "contents_checked": False}


def inspect(path):
    path = path.resolve()
    doc, container, file_size, chunks, binary_size = read_document(path)
    warnings = []
    errors = []
    resources = []
    buffers = doc.get("buffers", [])
    for kind in ("buffers", "images"):
        for index, resource in enumerate(doc.get(kind, [])):
            record = {"kind": kind, "index": index}
            if "uri" in resource:
                record.update(resource_status(resource["uri"], path.parent))
                if record["storage"] == "local-file" and not record["exists"]:
                    errors.append("Missing {} resource {}".format(kind, index))
                if record["storage"] not in ("data-uri", "local-file"):
                    warnings.append("{} resource {} is external or needs packaging review".format(kind, index))
                if kind == "buffers" and record.get("exists"):
                    expected = integer(resource.get("byteLength"), "buffer byteLength")
                    if record["bytes"] < expected:
                        errors.append("Local buffer {} is shorter than byteLength".format(index))
            elif kind == "images" and "bufferView" in resource:
                item(doc.get("bufferViews", []), resource["bufferView"], "image bufferView")
                record.update({"storage": "buffer-view", "contents_checked": False})
            elif kind == "buffers" and index == 0 and binary_size is not None:
                expected = integer(resource.get("byteLength"), "buffer byteLength")
                if not expected <= binary_size <= expected + 3:
                    errors.append("GLB BIN size does not match buffer 0 plus padding")
                record.update({"storage": "glb-bin", "bytes": binary_size, "contents_checked": False})
            else:
                errors.append("{} resource {} has no readable storage declaration".format(kind, index))
                record["storage"] = "missing"
            resources.append(record)

    for index, view in enumerate(doc.get("bufferViews", [])):
        buffer = item(buffers, view.get("buffer"), "bufferView buffer")
        end = integer(view.get("byteOffset", 0), "bufferView offset") + integer(view.get("byteLength"), "bufferView length")
        if end > integer(buffer.get("byteLength"), "buffer byteLength"):
            errors.append("bufferView {} exceeds its declared buffer".format(index))

    accessors = doc.get("accessors", [])
    geometry = []
    triangle_total = 0
    for mesh_index, mesh in enumerate(doc.get("meshes", [])):
        for primitive_index, primitive in enumerate(mesh.get("primitives", [])):
            mode = primitive.get("mode", 4)
            position_index = primitive.get("attributes", {}).get("POSITION")
            position = item(accessors, position_index, "POSITION accessor") if position_index is not None else None
            vertices = integer(position.get("count"), "POSITION count") if position is not None else None
            if "indices" in primitive:
                count = integer(item(accessors, primitive["indices"], "indices accessor").get("count"), "indices count")
            else:
                count = vertices
            if mode == 4 and count is not None:
                triangles = count // 3
                if count % 3:
                    errors.append("Triangle primitive {}:{} has a count not divisible by 3".format(mesh_index, primitive_index))
            elif mode in (5, 6) and count is not None:
                triangles = max(0, count - 2)
            else:
                triangles = None
            triangle_total += triangles or 0
            record = {"mesh": mesh_index, "primitive": primitive_index, "mode": mode,
                      "position_vertices": vertices, "nominal_triangles": triangles,
                      "material": primitive.get("material"), "morph_targets": len(primitive.get("targets", []))}
            if position is not None and "min" in position and "max" in position:
                record["declared_local_position_bounds"] = {"min": position["min"], "max": position["max"]}
            geometry.append(record)

    warnings.append("Geometry counts are per mesh definition, not world-space, instanced, visible-scene, or draw-call counts; degenerate triangles are not decoded.")
    if doc.get("extensionsRequired"):
        warnings.append("Confirm required extensions and decoders in the target loader.")
    if any(chunk["type"] not in ("0x4e4f534a", "0x4e4942") for chunk in chunks):
        warnings.append("GLB contains unknown chunks; review with the Khronos validator.")
    embedded_only = all(r["storage"] in ("data-uri", "buffer-view", "glb-bin") for r in resources)
    return {
        "file": str(path), "container": container, "file_bytes": file_size,
        "scope": "inventory and limited structural checks; NOT full glTF validation or visual verification",
        "generator": doc.get("asset", {}).get("generator"), "chunks": chunks,
        "scenes": len(doc.get("scenes", [])), "nodes": len(doc.get("nodes", [])),
        "meshes": len(doc.get("meshes", [])), "primitives": len(geometry),
        "nominal_mesh_definition_triangles": triangle_total,
        "materials": len(doc.get("materials", [])), "textures": len(doc.get("textures", [])),
        "images": len(doc.get("images", [])),
        "animations": [{"name": a.get("name", "animation-{}".format(i)), "channels": len(a.get("channels", []))}
                       for i, a in enumerate(doc.get("animations", []))],
        "skins": [{"name": s.get("name", "skin-{}".format(i)), "joints": len(s.get("joints", []))}
                  for i, s in enumerate(doc.get("skins", []))],
        "extensions_used": doc.get("extensionsUsed", []), "extensions_required": doc.get("extensionsRequired", []),
        "declared_embedded_resources_only": embedded_only and not errors,
        "resources": resources, "geometry": geometry, "warnings": warnings, "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset", type=Path, help="Path to a GLB or .gltf file")
    args = parser.parse_args()
    try:
        report = inspect(args.asset)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        # Avoid reflecting malformed JSON/URI contents or binary data into logs.
        print(json.dumps({"error": "Unable to inspect asset", "error_type": type(exc).__name__}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
