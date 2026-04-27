#!/usr/bin/env python3
"""
One-shot migration: convert OLD-format ScentBar presets to the NEW schema.

Old format (input):
  { kind, version, preset, exportedAt, label?, snapshot: { global, slots[] } }
  slot keys: labels, threshold, enabled, color, intensity, dutyPercent, cooldown

New format (output):
  { version, key, name, global, slots[] }
  slot keys: value, display, labels, threshold, enabled, color,
             intensity, dutyPercent, cooldown

For each slot the scent is derived from the first label, matched
case-insensitively against scents.json (e.g. "Gunpowder" -> id "gunpowder").
Unmatched slots are reported and the file is skipped.
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENTS_FILE = ROOT / "scents.json"
TARGET_DIR = ROOT / "presets"


def load_scents():
    """Return dict mapping lowercase name AND id -> (id, name)."""
    data = json.loads(SCENTS_FILE.read_text(encoding="utf-8"))
    lookup = {}
    for s in data.get("scents", []):
        sid, name = s["id"], s["name"]
        lookup[name.lower()] = (sid, name)
        lookup[sid.lower()] = (sid, name)
    return lookup


def slug_from_preset_key(key, fallback):
    """custom-7daystodie -> 7daystodie"""
    if isinstance(key, str) and key.startswith("custom-"):
        return key[len("custom-"):]
    return fallback


def name_from_slug(slug):
    """7daystodie -> '7daystodie' (leave as-is, user can polish later)"""
    return slug.replace("-", " ").strip() or slug


def migrate_one(src_path, scents):
    raw = json.loads(Path(src_path).read_text(encoding="utf-8"))

    # --- top level ---
    old_key = raw.get("preset", "")
    file_slug = Path(src_path).stem.replace("sb-preset-", "")
    slug = slug_from_preset_key(old_key, file_slug).lower()
    if not slug:
        slug = file_slug.lower()
    new_key = f"custom-{slug}"

    name = raw.get("label") or name_from_slug(slug)

    # --- global ---
    g_old = raw.get("snapshot", {}).get("global", {}) or {}
    new_global = {
        "intensity":   int(g_old.get("intensity", 4)),
        "threshold":   int(g_old.get("threshold", 75)),
        "dutyPercent": int(g_old.get("dutyPercent", 100)),
        "cooldown":    int(g_old.get("cooldown", 8)),
    }

    # --- slots ---
    new_slots = []
    warnings = []
    for i, slot in enumerate(raw.get("snapshot", {}).get("slots", []) or []):
        labels = slot.get("labels") or []
        if not labels:
            warnings.append(f"slot[{i}]: no labels")
            continue

        # find scent: first label lookup, then any label
        chosen = None
        for lbl in labels:
            hit = scents.get(str(lbl).lower().strip())
            if hit:
                chosen = hit
                break
        if not chosen:
            warnings.append(
                f"slot[{i}]: no scent match for labels {labels[:3]!r}"
            )
            continue

        scent_id, scent_name = chosen

        # ensure ≥3 labels: if too few, just pad-skip (warn)
        # de-duplicate (case-insensitive) preserving order
        seen, clean = set(), []
        for lbl in labels:
            k = str(lbl).strip().lower()
            if k and k not in seen:
                seen.add(k)
                clean.append(str(lbl).strip())
        if len(clean) < 3:
            warnings.append(f"slot[{i}]: only {len(clean)} labels (<3)")

        new_slots.append({
            "value":       scent_id,
            "display":     scent_name,
            "labels":      clean,
            "threshold":   int(slot.get("threshold", new_global["threshold"])),
            "enabled":     bool(slot.get("enabled", True)),
            "color":       slot.get("color", "#888888"),
            "intensity":   int(slot.get("intensity", new_global["intensity"])),
            "dutyPercent": int(slot.get("dutyPercent", new_global["dutyPercent"])),
            "cooldown":    int(slot.get("cooldown", new_global["cooldown"])),
        })

    new_doc = {
        "version": 1,
        "key":     new_key,
        "name":    name,
        "global":  new_global,
        "slots":   new_slots,
    }
    return new_doc, warnings, slug


def main():
    p = argparse.ArgumentParser()
    p.add_argument("source_dir", help="Folder with old-format presets")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--overwrite", action="store_true",
                   help="Replace files in presets/ that already exist")
    args = p.parse_args()

    src = Path(args.source_dir).resolve()
    if not src.is_dir():
        print(f"::error::Not a folder: {src}")
        return 1

    scents = load_scents()
    files = sorted(src.glob("sb-preset-*.json"))
    if not files:
        print(f"No sb-preset-*.json files in {src}")
        return 1

    print(f"Migrating {len(files)} preset(s) from {src}")
    print(f"           into {TARGET_DIR}")
    print(f"Scent catalog: {len(scents)//2} scents loaded\n")

    skipped, written, warned = 0, 0, 0
    TARGET_DIR.mkdir(exist_ok=True)

    for f in files:
        try:
            new_doc, warnings, slug = migrate_one(f, scents)
        except Exception as e:
            print(f"  X {f.name}: {e}")
            skipped += 1
            continue

        target = TARGET_DIR / f"sb-preset-{slug}.json"
        if target.exists() and not args.overwrite:
            print(f"  - {f.name}: target {target.name} exists - skipping (use --overwrite)")
            skipped += 1
            continue

        if warnings:
            warned += 1
            print(f"  ! {f.name} -> {target.name}")
            for w in warnings:
                print(f"      {w}")
        else:
            print(f"  + {f.name} -> {target.name}")

        if not args.dry_run:
            target.write_text(
                json.dumps(new_doc, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            written += 1

    print()
    print(f"Done. written={written}  skipped={skipped}  with-warnings={warned}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
