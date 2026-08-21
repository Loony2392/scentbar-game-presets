#!/usr/bin/env python3
"""
Validate all ScentBar preset files.

Checks:
  1. Valid JSON syntax
    2. Required top-level keys: version, key, name, slots
  3. version == 1
  4. key matches ^custom-[a-z0-9-]+$
    5. Each slot has required keys with valid types/ranges
    6. slot.value matches a scent.id from scents.json
    7. slot.display matches the matching scent.name
    8. slot.labels: minimum 4, no empty strings, no duplicates (case-insensitive)
    9. Color values are valid hex (#RRGGBB)

Exit code 0 = all valid, 1 = errors found.
"""

import json
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENTS_FILE = os.path.join(ROOT, "scents.json")
PRESET_GLOB = os.path.join(ROOT, "presets", "sb-preset-*.json")

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
KEY_RE = re.compile(r"^custom-[a-z0-9-]+$")

REQUIRED_TOP = {"version", "key", "name", "slots"}
REQUIRED_SLOT = {
    "value", "display", "labels",
    "threshold", "enabled", "color",
    "intensity", "dutyPercent", "cooldown",
}


def load_scents():
    """Return {scent_id: scent_name} from scents.json."""
    if not os.path.exists(SCENTS_FILE):
        return {}
    with open(SCENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {s["id"]: s["name"] for s in data.get("scents", [])}


def check_int(value, lo, hi, label):
    if not isinstance(value, int) or isinstance(value, bool):
        return [f"{label}={value!r} must be an integer"]
    if value < lo or value > hi:
        return [f"{label}={value} out of range ({lo}–{hi})"]
    return []


def validate_slot(slot, idx, scents):
    errors = []
    p = f"slots[{idx}]"

    if not isinstance(slot, dict):
        return [f"{p}: not an object"]

    missing = REQUIRED_SLOT - set(slot.keys())
    if missing:
        errors.append(f"{p}: missing keys {sorted(missing)}")
    extra = set(slot.keys()) - REQUIRED_SLOT
    if extra:
        errors.append(f"{p}: unknown keys {sorted(extra)}")

    # value -> scents.id
    value = slot.get("value")
    if not isinstance(value, str) or not re.match(r"^[a-z][a-z0-9-]*$", value or ""):
        errors.append(f"{p}.value={value!r} invalid (lowercase id required)")
    elif scents and value not in scents:
        errors.append(f"{p}.value='{value}' not found in scents.json")

    # display matches scent name
    display = slot.get("display")
    if not isinstance(display, str) or not display.strip():
        errors.append(f"{p}.display empty")
    elif scents and value in scents and display != scents[value]:
        errors.append(
            f"{p}.display='{display}' does not match scents.json name '{scents[value]}'"
        )

    # labels
    labels = slot.get("labels")
    if not isinstance(labels, list):
        errors.append(f"{p}.labels must be an array")
    else:
        if len(labels) < 4:
            errors.append(f"{p}.labels has {len(labels)} entries (minimum 4)")
        for i, lbl in enumerate(labels):
            if not isinstance(lbl, str) or not lbl.strip():
                errors.append(f"{p}.labels[{i}] empty or not a string")
        seen = set()
        for lbl in labels:
            if isinstance(lbl, str):
                key = lbl.lower().strip()
                if key in seen:
                    errors.append(f"{p}: duplicate label '{lbl}'")
                seen.add(key)

    # numeric ranges
    errors += check_int(slot.get("threshold"),   0, 100, f"{p}.threshold")
    errors += check_int(slot.get("intensity"),   1, 10,  f"{p}.intensity")
    errors += check_int(slot.get("dutyPercent"), 1, 100, f"{p}.dutyPercent")
    cd = slot.get("cooldown")
    if not isinstance(cd, int) or isinstance(cd, bool) or cd < 1:
        errors.append(f"{p}.cooldown={cd!r} must be integer >= 1")

    # enabled
    if not isinstance(slot.get("enabled"), bool):
        errors.append(f"{p}.enabled must be boolean")

    # color
    color = slot.get("color", "")
    if not isinstance(color, str) or not HEX_RE.match(color):
        errors.append(f"{p}.color='{color}' invalid (expected #RRGGBB)")

    return errors


def validate_preset(filepath, scents):
    errors = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]

    if not isinstance(data, dict):
        return ["root is not an object"]

    missing = REQUIRED_TOP - set(data.keys())
    if missing:
        errors.append(f"missing top-level keys {sorted(missing)}")
    extra = set(data.keys()) - REQUIRED_TOP
    if extra:
        errors.append(f"unknown top-level keys {sorted(extra)}")

    if data.get("version") != 1:
        errors.append(f"version={data.get('version')!r} must be 1")

    key = data.get("key", "")
    if not isinstance(key, str) or not KEY_RE.match(key):
        errors.append(f"key='{key}' must match ^custom-[a-z0-9-]+$")

    name = data.get("name", "")
    if not isinstance(name, str) or not name.strip():
        errors.append("name is empty")

    slots = data.get("slots", [])
    if not isinstance(slots, list):
        errors.append("slots must be an array")
    elif not slots:
        errors.append("slots is empty (need at least 1)")
    else:
        for i, slot in enumerate(slots):
            errors.extend(validate_slot(slot, i, scents))

    return errors


def main():
    files = sorted(glob.glob(PRESET_GLOB))
    if not files:
        print("::warning::No preset files found in presets/")
        return 0

    scents = load_scents()
    if scents:
        print(f"Loaded {len(scents)} scents from scents.json")
    else:
        print("::warning::scents.json missing or empty — skipping scent reference checks")

    print(f"Validating {len(files)} preset(s)...\n")
    failed = 0
    total_errors = 0

    for path in files:
        name = os.path.basename(path)
        errors = validate_preset(path, scents)
        if errors:
            failed += 1
            total_errors += len(errors)
            print(f"FAIL  {name}")
            for e in errors:
                print(f"      {e}")
                print(f"::error file=presets/{name}::{e}")
        else:
            print(f"OK    {name}")

    print()
    print(f"Summary: {len(files) - failed}/{len(files)} valid, {total_errors} error(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
