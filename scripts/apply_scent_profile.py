"""Apply per-scent default profile (derived from hand-tuned reference presets)
to all other presets. Updates only dutyPercent and cooldown per slot.
Leaves global section untouched. Skips reference presets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRESETS = ROOT / "presets"

REF = {"battlefield6", "minecraft", "the-elder-scrolls", "cyberpunk2077"}

# scent -> (dutyPercent, cooldown)
# Cooldown-Logik: je haeufiger / dauerhafter ein Duft typischerweise getriggert
# wird, desto laenger der Cooldown -- vermeidet Uebersaettigung.
PROFILE = {
    # Dauer-Ambient (Biome/Umgebung, fast immer sichtbar) -> hoher Cooldown
    "forest":    (100, 14),
    "grass":     (80, 14),
    "dirt":      (90, 14),
    "cave":      (100, 14),
    "sea":       (80, 14),
    "snow":      (60, 14),
    "desert":    (100, 14),
    "smoke":     (100, 12),
    # Haeufige Action (Shooter etc.) -> mittlerer Cooldown
    "gunpowder": (100, 10),
    "rain":      (100, 12),
    # Gelegentlich (situativ, kurz) -> Standard-Cooldown
    "leather":   (60, 10),
    "leaves":    (60, 10),
    "hay":       (100, 10),
    "energy":    (80, 10),
    "brakes":    (80, 10),
    "temple":    (80, 12),
    # Selten / Event (Highlights, kurze Bursts) -> kurzer Cooldown
    "victory":   (100, 8),
    "health":    (100, 8),
    "perfume":   (100, 10),
    "coffee":    (100, 10),
    "flowers":   (60, 16),
    "new-car":   (60, 30),
    "bakery":    (100, 12),
}

changed = 0
for f in sorted(PRESETS.glob("sb-preset-*.json")):
    stem = f.stem.replace("sb-preset-", "")
    if stem in REF:
        continue
    p = json.loads(f.read_text(encoding="utf8"))
    modified = False
    for s in p.get("slots", []):
        v = s.get("value")
        if v in PROFILE:
            duty, cool = PROFILE[v]
            if s.get("dutyPercent") != duty or s.get("cooldown") != cool:
                s["dutyPercent"] = duty
                s["cooldown"] = cool
                modified = True
    if modified:
        f.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
        changed += 1
        print(f"  updated {f.name}")

print(f"\nDone. {changed} preset(s) updated.")
