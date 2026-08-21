# ScentBar Game Presets

[![Validate Presets](https://github.com/loony2392/scentbar-game-presets/actions/workflows/validate.yml/badge.svg)](https://github.com/loony2392/scentbar-game-presets/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

![ZESTUM - Trailer](assets/zestum_trailer.gif)

Community-built scent presets for the **[ScentBar by Zestum](https://zestum.tech/)** —
the hardware that diffuses real-world scents synced to what's happening on your
screen.

> 🌐 **Browse the catalogue:** <https://loony2392.github.io/scentbar-game-presets/>

---

## What's a preset?

A small JSON file mapping AI-vision keywords (what the camera sees on your
screen) to ScentPods. Drop it into the ScentBar app and the bar fires the right
scent at the right moment — gunpowder when you shoot, forest when you're in the
woods, victory when you win.

## How to use a preset

1. Pick a preset from [`presets/`](presets/) — or grab everything in one shot:
   [`all-presets.json`](all-presets.json) *(auto-generated on every merge)*
2. Open the **ScentBar app** → *Presets* → **Import**
3. Pick the JSON file → done

The official ScentBar app and ScentPods are available at
**[zestum.tech](https://zestum.tech/)**.

## Available presets

<!-- PRESETS:START -->
**16 presets** available:

| Game | File | Slots |
|------|------|-------|
| Apex Legends | [`presets/sb-preset-apex-legends.json`](presets/sb-preset-apex-legends.json) | 10 |
| Battlefield 6 | [`presets/sb-preset-battlefield6.json`](presets/sb-preset-battlefield6.json) | 10 |
| Call of Duty | [`presets/sb-preset-call-of-duty.json`](presets/sb-preset-call-of-duty.json) | 10 |
| Counter-Strike 2 | [`presets/sb-preset-counter-strike-2.json`](presets/sb-preset-counter-strike-2.json) | 10 |
| Cyberpunk 2077 | [`presets/sb-preset-cyberpunk2077.json`](presets/sb-preset-cyberpunk2077.json) | 10 |
| Dota 2 | [`presets/sb-preset-dota-2.json`](presets/sb-preset-dota-2.json) | 10 |
| Fortnite | [`presets/sb-preset-fortnite.json`](presets/sb-preset-fortnite.json) | 10 |
| GTA 5 | [`presets/sb-preset-gta-5.json`](presets/sb-preset-gta-5.json) | 10 |
| Helldivers 2 | [`presets/sb-preset-helldivers-2.json`](presets/sb-preset-helldivers-2.json) | 10 |
| League of Legends | [`presets/sb-preset-league-of-legends.json`](presets/sb-preset-league-of-legends.json) | 10 |
| Minecraft | [`presets/sb-preset-minecraft.json`](presets/sb-preset-minecraft.json) | 10 |
| Overwatch 2 | [`presets/sb-preset-overwatch-2.json`](presets/sb-preset-overwatch-2.json) | 10 |
| Rainbow Six Siege | [`presets/sb-preset-rainbow-six-siege.json`](presets/sb-preset-rainbow-six-siege.json) | 10 |
| The Elder Scrolls | [`presets/sb-preset-the-elder-scrolls.json`](presets/sb-preset-the-elder-scrolls.json) | 10 |
| Valorant | [`presets/sb-preset-valorant.json`](presets/sb-preset-valorant.json) | 10 |
| World of Warcraft | [`presets/sb-preset-world-of-warcraft.json`](presets/sb-preset-world-of-warcraft.json) | 10 |
<!-- PRESETS:END -->

More games are coming. **PRs very welcome** — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Available scents

<!-- SCENTS:START -->
**23 ScentPods**
<!-- SCENTS:END --> are referenced. The full catalogue with descriptions, colors and
categories lives in [`scents.json`](scents.json) — that's also the source of
truth for the validator.

## Preset format (short version)

```json
{
  "version": 1,
  "key": "custom-<slug>",
  "name": "<Game Title>",
  "global":  { "intensity": 4, "threshold": 75, "dutyPercent": 100, "cooldown": 8 },
  "slots":   [
    {
      "value": "gunpowder",
      "display": "Gunpowder",
      "labels": ["gunpowder", "explosion", "muzzle flash"],
      "threshold": 74,
      "enabled": true,
      "color": "#616161",
      "intensity": 4,
      "dutyPercent": 80,
      "cooldown": 8
    }
  ]
}
```

Rules: `key` must match `^custom-[a-z0-9-]+$`, every `value` must exist in
`scents.json`, and **every slot needs at least 3 unique labels**. Full spec in
[CONTRIBUTING.md](CONTRIBUTING.md) and
[`schemas/preset-schema.json`](schemas/preset-schema.json).

## Repository layout

```
presets/                  # one JSON file per game
scents.json               # canonical list of all available ScentPods
schemas/
  preset-schema.json      # JSON Schema (draft-07) for presets
  scents-schema.json      # JSON Schema for scents.json
scripts/
  validate_presets.py     # local + CI validator
  generate_bundle.py      # rebuilds all-presets.json
all-presets.json          # auto-generated bundle of every preset
docs/                     # GitHub Pages landing site
```

## Validate locally

```bash
pip install jsonschema
python scripts/validate_presets.py
```

CI runs the same checks plus a strict JSON-Schema pass on every PR.

## Contributing

Open a PR with your preset under `presets/`. The CI will validate it
automatically. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## Disclaimer

This is a **community project** and is **not affiliated with Zestum**.
"ScentBar", "Zestum" and product names belong to their respective owners.

## License

[MIT](LICENSE)
