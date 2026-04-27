"""Analyze the 4 hand-tuned presets to derive per-scent default settings."""
import json
from collections import defaultdict
from pathlib import Path

REFS = ["battlefield6", "minecraft", "the-elder-scrolls", "cyberpunk2077"]
ROOT = Path(__file__).resolve().parents[1]

per_scent = defaultdict(list)  # scent -> list of (duty, cooldown, threshold, intensity)
globals_seen = []

for ref in REFS:
    p = json.loads((ROOT / "presets" / f"sb-preset-{ref}.json").read_text(encoding="utf8"))
    g = p["global"]
    globals_seen.append((ref, g))
    print(f"=== {ref} ===")
    print(f"  GLOBAL  int={g['intensity']}  thr={g['threshold']}  dut={g['dutyPercent']}  cool={g['cooldown']}")
    for s in p["slots"]:
        print(f"    {s['value']:12} dut={s['dutyPercent']:3}  cool={s['cooldown']:3}  thr={s['threshold']:3}  int={s['intensity']}")
        per_scent[s["value"]].append((s["dutyPercent"], s["cooldown"], s["threshold"], s["intensity"]))

print("\n=== PER-SCENT AVERAGES (n samples) ===")
for scent in sorted(per_scent):
    rows = per_scent[scent]
    n = len(rows)
    avg_d = round(sum(r[0] for r in rows) / n)
    avg_c = round(sum(r[1] for r in rows) / n)
    avg_t = round(sum(r[2] for r in rows) / n)
    avg_i = round(sum(r[3] for r in rows) / n)
    print(f"  {scent:12} n={n}  dut={avg_d:3}  cool={avg_c:3}  thr={avg_t:3}  int={avg_i}")
