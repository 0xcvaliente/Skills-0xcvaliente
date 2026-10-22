#!/usr/bin/env python3
"""Validate a pptx-deck specification (JSON) against the schema and the deck rules.

Checks performed
----------------
1. JSON Schema validation against references/deck-spec.schema.json (uses the
   `jsonschema` package when installed, otherwise a built-in validator that
   covers type / const / enum / pattern / required / additionalProperties /
   items / minItems / maxItems / minLength / minimum / maximum / $ref).
2. The semantic rules in the schema's `x-rules`, `x-roleLimits`,
   `x-densityLimits` and `x-sameRoleRun` sections: exactly one cover (first) and
   one closing (last), unique ids and media paths, character caps for full and
   short texts, item caps (role and density), chart and media permissions,
   required fields, layout variant range, chart series length, theme/seed
   consistency, auto-pick restriction, and so on.
3. Warnings: missing speaker notes, long runs of the same role+variant, media
   files that cannot be found, slide count versus durationMinutes, chart
   insight numbers that do not match the data, and similar quality hints.

Exit status: 0 when there are no errors (warnings are fine), 1 when there is at
least one error, 2 when the spec file cannot be read.

Optional spec key `themeChosenBy: "user"` (not part of the JSON schema; it is
removed before schema validation) records that the person explicitly asked for
a theme with autoPick=false (for example ledger-gold); without it such a theme
produces a warning.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

# Keys that may appear in a spec file but are not part of the schema.
EXTRA_TOP_LEVEL_KEYS = ("$schema", "themeChosenBy")


class Issue:
    """One validation finding."""

    def __init__(self, level: str, code: str, path: str, message: str) -> None:
        self.level = level  # "error" or "warning"
        self.code = code
        self.path = path
        self.message = message

    def as_dict(self) -> Dict[str, str]:
        return {"level": self.level, "code": self.code, "path": self.path, "message": self.message}

    def __str__(self) -> str:
        loc = ("[%s] " % self.path) if self.path else ""
        return "%s %s%s (%s)" % (self.level.upper(), loc, self.message, self.code)


# --------------------------------------------------------------------------
# Built-in JSON Schema validator (subset)
# --------------------------------------------------------------------------


def _type_ok(value: Any, tname: str) -> bool:
    if tname == "object":
        return isinstance(value, dict)
    if tname == "array":
        return isinstance(value, list)
    if tname == "string":
        return isinstance(value, str)
    if tname == "boolean":
        return isinstance(value, bool)
    if tname == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if tname == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if tname == "null":
        return value is None
    return True


def _resolve_ref(root: Dict[str, Any], ref: str) -> Dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError("Only local $ref supported: %s" % ref)
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def builtin_validate(value: Any, schema: Dict[str, Any], root: Dict[str, Any], path: str = "") -> List[Tuple[str, str]]:
    """Validate *value* against *schema*; return a list of ``(path, message)`` errors."""
    errs: List[Tuple[str, str]] = []
    if "$ref" in schema:
        return builtin_validate(value, _resolve_ref(root, schema["$ref"]), root, path)

    def add(msg: str) -> None:
        errs.append((path, msg))

    if "const" in schema and value != schema["const"]:
        add("must equal %r" % (schema["const"],))
        return errs
    if "enum" in schema and value not in schema["enum"]:
        add("must be one of %s (got %r)" % (", ".join(repr(x) for x in schema["enum"]), value))
        return errs
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(value, t) for t in types):
            add("must be of type %s (got %s)" % ("/".join(types), type(value).__name__))
            return errs

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            add("must have at least %d character(s)" % schema["minLength"])
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            add("must have at most %d characters" % schema["maxLength"])
        if "pattern" in schema and not re.search(schema["pattern"], value):
            add("does not match pattern %s" % schema["pattern"])
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            add("must be >= %s" % schema["minimum"])
        if "maximum" in schema and value > schema["maximum"]:
            add("must be <= %s" % schema["maximum"])
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            add("must have at least %d item(s)" % schema["minItems"])
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            add("must have at most %d item(s)" % schema["maxItems"])
        if "items" in schema:
            for i, el in enumerate(value):
                errs.extend(builtin_validate(el, schema["items"], root, "%s[%d]" % (path, i)))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in value:
                add("missing required property %r" % req)
        ap = schema.get("additionalProperties", True)
        for k, v in value.items():
            sub = "%s.%s" % (path, k) if path else k
            if k in props:
                errs.extend(builtin_validate(v, props[k], root, sub))
            elif ap is False:
                errs.append((sub, "unknown property %r (additionalProperties is false)" % k))
            elif isinstance(ap, dict):
                errs.extend(builtin_validate(v, ap, root, sub))
    return errs


def schema_errors(spec: Any, use_jsonschema: bool = True) -> Tuple[List[Tuple[str, str]], str]:
    """Return ``(errors, engine)`` for schema validation. engine is 'jsonschema' or 'builtin'."""
    schema = C.load_schema()
    if use_jsonschema:
        try:
            import jsonschema  # type: ignore

            validator = jsonschema.Draft202012Validator(schema)
            out = []
            for e in sorted(validator.iter_errors(spec), key=lambda x: [str(p) for p in x.absolute_path]):
                p = ""
                for part in e.absolute_path:
                    p += "[%d]" % part if isinstance(part, int) else ("." + str(part) if p else str(part))
                out.append((p, e.message))
            return out, "jsonschema"
        except ImportError:
            pass
    return builtin_validate(spec, schema, schema), "builtin"


# --------------------------------------------------------------------------
# Semantic checks
# --------------------------------------------------------------------------

_NUM_RE = re.compile(r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?")


def _numbers_in(text: str) -> List[float]:
    out = []
    for m in _NUM_RE.finditer(text):
        raw = m.group(0).replace(",", "")
        try:
            out.append(float(raw))
        except ValueError:
            continue
    return out


def _derived_numbers(chart: Dict[str, Any]) -> List[float]:
    """Numbers a truthful insight may quote: values, sums, differences, ratios, percent shares and changes."""
    vals: List[float] = []
    series = [s.get("values", []) for s in chart.get("series", []) if isinstance(s, dict)]
    flat = [v for s in series for v in s if isinstance(v, (int, float))]
    vals.extend(flat)
    for s in series:
        nums = [v for v in s if isinstance(v, (int, float))]
        if nums:
            vals += [sum(nums), max(nums), min(nums), sum(nums) / len(nums)]
            total = sum(nums)
            if total:
                vals += [v / total * 100 for v in nums]
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i == j:
                    continue
                a, b = nums[i], nums[j]
                vals.append(abs(a - b))
                if b:
                    vals += [a / b, (a - b) / b * 100, abs(a - b) / abs(b) * 100]
    if series:
        n = max(len(s) for s in series)
        for k in range(n):
            col = [s[k] for s in series if k < len(s) and isinstance(s[k], (int, float))]
            if col:
                vals.append(sum(col))
                tot = sum(col)
                if tot:
                    vals += [v / tot * 100 for v in col]
        # cross-series comparisons for the same category
        for k in range(n):
            col = [s[k] for s in series if k < len(s) and isinstance(s[k], (int, float))]
            for a in col:
                for b in col:
                    if a != b:
                        vals.append(abs(a - b))
                        if b:
                            vals += [a / b, (a - b) / b * 100, abs(a - b) / abs(b) * 100]
    return vals


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= max(0.51, abs(b) * 0.011) if abs(b) >= 1 else abs(a - b) <= 0.051


def _g(d: Any, key: str, default: Any = None) -> Any:
    return d.get(key, default) if isinstance(d, dict) else default


def _text_len(obj: Any, which: str) -> Optional[int]:
    if isinstance(obj, dict) and isinstance(obj.get(which), str):
        return len(obj[which])
    return None


def semantic_checks(spec: Dict[str, Any], spec_dir: Path) -> List[Issue]:
    """Run the x-rules on a (schema-shaped) spec and return Issues."""
    issues: List[Issue] = []

    def err(code: str, path: str, msg: str) -> None:
        issues.append(Issue("error", code, path, msg))

    def warn(code: str, path: str, msg: str) -> None:
        issues.append(Issue("warning", code, path, msg))

    schema = C.load_schema()
    limits = schema["x-roleLimits"]
    slides = spec.get("slides")
    if not isinstance(slides, list):
        return issues

    # ---- theme / seed -------------------------------------------------
    theme_id = spec.get("theme")
    theme = None
    if isinstance(theme_id, str):
        try:
            theme = C.get_theme(theme_id)
        except KeyError as exc:
            err("theme-unknown", "theme", str(exc.args[0]))
    seed = spec.get("randomSeed")
    if isinstance(seed, str) and isinstance(theme_id, str):
        prefix = C.seed_theme_prefix(seed)
        if prefix is not None and prefix != theme_id:
            err("seed-theme", "randomSeed", "randomSeed prefix %r must equal theme %r" % (prefix, theme_id))
    if theme is not None and theme.get("autoPick") is False:
        if spec.get("themeChosenBy") != "user":
            warn(
                "theme-explicit-only",
                "theme",
                "theme %r has autoPick=false: use it only when the user explicitly asked for it "
                "(set \"themeChosenBy\": \"user\" in the spec to record that)" % theme_id,
            )

    density = spec.get("density") or "speaker-led"

    # ---- cover / closing ---------------------------------------------
    roles = [_g(s, "role") for s in slides]
    n = len(slides)
    cover_idx = [i for i, r in enumerate(roles) if r == "cover"]
    close_idx = [i for i, r in enumerate(roles) if r == "closing"]
    if len(cover_idx) != 1:
        err("cover-count", "slides", "expected exactly one cover slide, found %d" % len(cover_idx))
    if len(close_idx) != 1:
        err("closing-count", "slides", "expected exactly one closing slide, found %d" % len(close_idx))
    if n and roles[0] != "cover":
        err("cover-first", "slides[0].role", "the first slide must be the cover (found %r)" % roles[0])
    if n and roles[-1] != "closing":
        err("closing-last", "slides[%d].role" % (n - 1), "the last slide must be the closing slide (found %r)" % roles[-1])
    if n == 1:
        err("too-few-slides", "slides", "a deck needs at least a cover and a closing slide")

    # ---- unique slide ids ---------------------------------------------
    seen_ids: Dict[str, int] = {}
    media_seen: Dict[str, int] = {}
    for i, s in enumerate(slides):
        base = "slides[%d]" % i
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        if isinstance(sid, str):
            if sid in seen_ids:
                err("slide-id-dup", base + ".id", "slide id %r already used by slide %d" % (sid, seen_ids[sid]))
            else:
                seen_ids[sid] = i
        role = s.get("role")
        lim = limits.get(role) if isinstance(role, str) else None
        if lim is None:
            continue
        caps = lim["maxChars"]

        # required fields
        for f in lim["requiredFields"]:
            v = s.get(f)
            empty = v is None or (isinstance(v, (str, list, dict)) and len(v) == 0)
            if f == "title" and isinstance(v, dict):
                empty = not (v.get("full") or "").strip() or not (v.get("short") or "").strip()
            if empty:
                err("required-field", base + "." + f, "role %r requires a non-empty %r" % (role, f))

        # text caps
        def check_text(obj: Any, path: str, cap_key: str) -> None:
            cap = caps[cap_key]
            full_len = _text_len(obj, "full")
            short_len = _text_len(obj, "short")
            if full_len is not None and full_len > cap:
                err("text-too-long", path + ".full", "%s is %d characters; role %r allows at most %d" % (cap_key, full_len, role, cap))
            if short_len is not None and short_len > C.short_limit(cap):
                err(
                    "short-too-long",
                    path + ".short",
                    "short %s is %d characters; must be at most %d (60%% of %d)" % (cap_key, short_len, C.short_limit(cap), cap),
                )

        if "title" in s:
            check_text(s["title"], base + ".title", "title")
        if "summary" in s:
            check_text(s["summary"], base + ".summary", "summary")

        # items
        items = s.get("items")
        if items is not None and isinstance(items, list):
            if len(items) > lim["maxItems"]:
                err("items-max", base + ".items", "role %r allows at most %d item(s); found %d" % (role, lim["maxItems"], len(items)))
            cap = C.density_cap(density, role)
            if role in schema["x-densityLimits"]["listLikeRoles"] and len(items) > cap >= 0 and len(items) <= lim["maxItems"]:
                err(
                    "density-cap",
                    base + ".items",
                    "density %r allows at most %d item(s) for role %r; found %d (split the slide)" % (density, cap, role, len(items)),
                )
            item_ids = set()
            for j, it in enumerate(items):
                ip = "%s.items[%d]" % (base, j)
                if not isinstance(it, dict):
                    continue
                iid = it.get("id")
                if isinstance(iid, str):
                    if iid in item_ids:
                        err("item-id-dup", ip + ".id", "item id %r repeated on this slide" % iid)
                    item_ids.add(iid)
                lab = it.get("label")
                if isinstance(lab, str) and len(lab) > caps["label"]:
                    err("text-too-long", ip + ".label", "label is %d characters; role %r allows at most %d" % (len(lab), role, caps["label"]))
                if "detail" in it:
                    check_text(it["detail"], ip + ".detail", "detail")
                dv = it.get("displayValue")
                if isinstance(dv, str) and len(dv) > 10:
                    warn("display-value-long", ip + ".displayValue", "displayValue %r is long; hero numbers should be 10 characters or fewer" % dv)

        # chart
        chart = s.get("chart")
        if chart is not None:
            if not lim["allowsChart"]:
                err("chart-not-allowed", base + ".chart", "role %r does not allow a chart" % role)
            if isinstance(chart, dict):
                cats = chart.get("categories")
                ser = chart.get("series")
                if isinstance(cats, list) and isinstance(ser, list):
                    for k, sr in enumerate(ser):
                        vals = _g(sr, "values")
                        if isinstance(vals, list) and len(vals) != len(cats):
                            err(
                                "chart-length",
                                "%s.chart.series[%d].values" % (base, k),
                                "series %r has %d value(s) but there are %d categories" % (_g(sr, "name", k), len(vals), len(cats)),
                            )
                    if chart.get("type") in ("pie", "doughnut") and len(ser) > 1:
                        warn("chart-pie-series", base + ".chart", "%s charts show one series; only the first is drawn" % chart["type"])
                    if len(cats) > 12:
                        warn("chart-many-categories", base + ".chart", "%d categories is hard to read; consider grouping" % len(cats))
                    ins = chart.get("insight")
                    if isinstance(ins, str):
                        allowed = _derived_numbers(chart)
                        cat_nums = [x for c in cats if isinstance(c, str) for x in _numbers_in(c)]
                        for num in _numbers_in(ins):
                            if any(_close(num, a) for a in allowed) or any(abs(num - c) < 1e-9 for c in cat_nums):
                                continue
                            if 1900 <= num <= 2100 and float(num).is_integer():
                                continue
                            warn("chart-insight-number", base + ".chart.insight", "insight quotes %g, which does not match the series values" % num)

        # media
        media = s.get("media")
        if media is not None:
            if not lim["allowsMedia"]:
                err("media-not-allowed", base + ".media", "role %r does not allow media" % role)
            if isinstance(media, list):
                for j, m in enumerate(media):
                    mp = "%s.media[%d]" % (base, j)
                    path = _g(m, "path")
                    if not isinstance(path, str):
                        continue
                    key = path.replace("\\", "/").lstrip("./") if not path.startswith("/") else path
                    if key in media_seen:
                        err("media-dup", mp + ".path", "media path %r is already used on slide %d" % (path, media_seen[key]))
                    else:
                        media_seen[key] = i
                    if re.match(r"^[a-z]+://", path):
                        warn("media-remote", mp + ".path", "remote URLs are not fetched; use a local file")
                        continue
                    resolved = Path(path) if Path(path).is_absolute() else (spec_dir / path)
                    if not resolved.is_file():
                        warn("media-missing", mp + ".path", "file not found: %s (a placeholder will be drawn)" % resolved)
                    elif resolved.suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"):
                        warn("media-format", mp + ".path", "%s is not a supported image format (png, jpg, gif, bmp, tiff)" % resolved.suffix)

        # layout variant
        lv = s.get("layoutVariant")
        if isinstance(lv, int) and not isinstance(lv, bool) and lv > lim["variants"]:
            err("variant-range", base + ".layoutVariant", "role %r has %d variant(s); layoutVariant %d is out of range" % (role, lim["variants"], lv))

        # notes
        if not (isinstance(s.get("notes"), str) and s["notes"].strip()):
            warn("notes-missing", base + ".notes", "slide %r has no speaker notes" % s.get("id", i))

    # ---- same role + variant runs -------------------------------------
    if all(isinstance(s, dict) and s.get("role") in limits for s in slides) and isinstance(spec.get("randomSeed"), str):
        maxrun = schema["x-sameRoleRun"]["maxConsecutiveSameRoleAndVariant"]
        pairs = []
        for i, s in enumerate(slides):
            try:
                pairs.append((s["role"], C.resolve_variant(spec, i)))
            except Exception:
                pairs.append((s["role"], None))
        run = 1
        for i in range(1, len(pairs)):
            run = run + 1 if pairs[i] == pairs[i - 1] and pairs[i][1] is not None else 1
            if run == maxrun + 1:
                warn(
                    "same-role-run",
                    "slides[%d]" % i,
                    "more than %d consecutive slides use role %r with layout variant %s" % (maxrun, pairs[i][0], pairs[i][1]),
                )
        run = 1
        for i in range(1, len(roles)):
            run = run + 1 if roles[i] == roles[i - 1] else 1
            if run == 4:
                warn("same-role-3", "slides[%d]" % i, "more than 3 consecutive slides use role %r; add a transition or ambient slide" % roles[i])

    # ---- pacing --------------------------------------------------------
    dur = spec.get("durationMinutes")
    if isinstance(dur, int) and not isinstance(dur, bool) and dur > 0:
        target = dur / schema["x-pacing"]["minutesPerSlide"]
        if n < target * 0.7 or n > target * 1.3:
            warn("pacing", "slides", "%d slides for %d minutes; about %.0f slides (%.1f min each) fits better" % (n, dur, target, schema["x-pacing"]["minutesPerSlide"]))

    # ---- template path -------------------------------------------------
    tpl = spec.get("template")
    if isinstance(tpl, str):
        tp = Path(tpl) if Path(tpl).is_absolute() else spec_dir / tpl
        if not tp.is_file():
            warn("template-missing", "template", "template file not found: %s" % tp)

    return issues


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------


def validate_spec(spec: Any, spec_dir: Path | str = ".", use_jsonschema: bool = True) -> Tuple[List[Issue], List[Issue]]:
    """Validate a parsed spec dict. Returns ``(errors, warnings)`` as lists of :class:`Issue`."""
    spec_dir = Path(spec_dir)
    issues: List[Issue] = []
    if not isinstance(spec, dict):
        return [Issue("error", "schema", "", "the spec must be a JSON object")], []
    cleaned = {k: v for k, v in spec.items() if k not in EXTRA_TOP_LEVEL_KEYS}
    errs, _engine = schema_errors(cleaned, use_jsonschema)
    for path, msg in errs:
        issues.append(Issue("error", "schema", path, msg))
    try:
        issues.extend(semantic_checks(spec, spec_dir))
    except Exception as exc:  # defensive: malformed spec shapes
        issues.append(Issue("error", "internal", "", "semantic checks aborted: %s: %s" % (type(exc).__name__, exc)))
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]
    return errors, warnings


def validate_file(path: Path | str, use_jsonschema: bool = True) -> Tuple[Optional[Dict[str, Any]], List[Issue], List[Issue]]:
    """Load and validate a spec file. Returns ``(spec_or_None, errors, warnings)``."""
    p = Path(path)
    try:
        spec = C.load_json(p)
    except FileNotFoundError:
        return None, [Issue("error", "io", "", "file not found: %s" % p)], []
    except json.JSONDecodeError as exc:
        return None, [Issue("error", "json", "", "invalid JSON: %s" % exc)], []
    errors, warnings = validate_spec(spec, p.resolve().parent, use_jsonschema)
    return spec, errors, warnings


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Validate a pptx-deck spec: JSON schema plus deck rules (role limits, density, "
        "cover/closing, media, charts, variants). Exit code 0 = no errors, 1 = errors, 2 = unreadable file.",
    )
    ap.add_argument("spec", help="path to the deck spec JSON file")
    ap.add_argument("--json", action="store_true", help="print a machine-readable JSON report instead of text")
    ap.add_argument("--no-jsonschema", action="store_true", help="always use the built-in schema validator even if the jsonschema package is installed")
    ap.add_argument("--quiet", "-q", action="store_true", help="text mode: print only errors and warnings, no summary line")
    args = ap.parse_args(argv)

    spec, errors, warnings = validate_file(args.spec, use_jsonschema=not args.no_jsonschema)
    unreadable = spec is None
    if args.json:
        report = {
            "ok": not errors,
            "spec": str(args.spec),
            "slides": len(spec.get("slides", [])) if isinstance(spec, dict) and isinstance(spec.get("slides"), list) else 0,
            "errorCount": len(errors),
            "warningCount": len(warnings),
            "errors": [e.as_dict() for e in errors],
            "warnings": [w.as_dict() for w in warnings],
        }
        print(json.dumps(report, indent=2))
    else:
        for e in errors:
            print(str(e))
        for w in warnings:
            print(str(w))
        if not args.quiet:
            print("%s: %d error(s), %d warning(s)" % ("FAIL" if errors else "OK", len(errors), len(warnings)))
    if unreadable:
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
