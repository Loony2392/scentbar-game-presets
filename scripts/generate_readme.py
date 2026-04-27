#!/usr/bin/env python3
"""
Update auto-generated sections in README.md:
  - <!-- PRESETS:START --> ... <!-- PRESETS:END -->
  - <!-- SCENTS:START -->  ... <!-- SCENTS:END -->

Other content is left untouched.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
SCENTS_FILE = os.path.join(ROOT, "scents.json")
PRESET_GLOB = os.path.join(ROOT, "presets", "sb-preset-*.json")

PRESETS_START = "<!-- PRESETS:START -->"
PRESETS_END = "<!-- PRESETS:END -->"
SCENTS_START = "<!-- SCENTS:START -->"
SCENTS_END = "<!-- SCENTS:END -->"


def load_presets():
    items = []
    for path in sorted(glob.glob(PRESET_GLOB)):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        items.append({
            "name": data.get("name") or os.path.basename(path),
            "file": os.path.basename(path),
            "slots": len(data.get("slots", [])),
        })
    items.sort(key=lambda e: e["name"].lower())
    return items


def load_scent_count():
    if not os.path.exists(SCENTS_FILE):
        return 0
    with open(SCENTS_FILE, "r", encoding="utf-8") as f:
        return len(json.load(f).get("scents", []))


def render_presets(items):
    if not items:
        return "_No presets yet — be the first to contribute!_"
    lines = [
        f"**{len(items)} preset{'s' if len(items) != 1 else ''}** available:",
        "",
        "| Game | File | Slots |",
        "|------|------|-------|",
    ]
    for it in items:
        lines.append(f"| {it['name']} | [`presets/{it['file']}`](presets/{it['file']}) | {it['slots']} |")
    return "\n".join(lines)


def render_scents(count):
    if count <= 0:
        return "_See [`scents.json`](scents.json)_"
    return f"**{count} ScentPods**"


def replace_block(content, start, end, new_inner):
    pattern = re.compile(
        rf"({re.escape(start)})(.*?)({re.escape(end)})",
        re.DOTALL,
    )
    if not pattern.search(content):
        print(f"::error::Markers '{start}' / '{end}' not found in README.md")
        return None
    return pattern.sub(rf"\1\n{new_inner}\n\3", content)


def main():
    if not os.path.exists(README):
        print("::error::README.md not found")
        return 1

    with open(README, "r", encoding="utf-8") as f:
        original = f.read()
    content = original

    items = load_presets()
    scent_count = load_scent_count()

    content = replace_block(content, PRESETS_START, PRESETS_END, render_presets(items))
    if content is None:
        return 1
    content = replace_block(content, SCENTS_START, SCENTS_END, render_scents(scent_count))
    if content is None:
        return 1

    if content == original:
        print(f"README.md already up to date — {len(items)} preset(s), {scent_count} scent(s)")
        return 0

    with open(README, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated README.md — {len(items)} preset(s), {scent_count} scent(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
