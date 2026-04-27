#!/usr/bin/env python3
"""Generate all-presets.json — a single bundle of every preset in presets/."""
import json
import glob
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESET_GLOB = os.path.join(ROOT, "presets", "sb-preset-*.json")
OUTPUT = os.path.join(ROOT, "all-presets.json")


def main():
    files = sorted(glob.glob(PRESET_GLOB))
    if not files:
        print("::warning::No presets found in presets/ — nothing to bundle")
        # still write an empty bundle so the file exists
    presets = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        presets.append(data)

    bundle = {
        "kind": "scentbar-preset-bundle",
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(presets),
        "presets": presets,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {os.path.relpath(OUTPUT, ROOT)} — {len(presets)} preset(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
