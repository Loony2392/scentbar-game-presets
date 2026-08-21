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
| Battlefield 6 - Experimental | [`presets/battlefield-6/sb-preset-battlefield6-experimental.json`](presets/battlefield-6/sb-preset-battlefield6-experimental.json) | 10 |
| Battlefield 6 - High Detail | [`presets/battlefield-6/sb-preset-battlefield6-high-detail.json`](presets/battlefield-6/sb-preset-battlefield6-high-detail.json) | 10 |
| Battlefield 6 - Performance | [`presets/battlefield-6/sb-preset-battlefield6-performance.json`](presets/battlefield-6/sb-preset-battlefield6-performance.json) | 10 |
| Battlefield 6 - Standard | [`presets/battlefield-6/sb-preset-battlefield6-standard.json`](presets/battlefield-6/sb-preset-battlefield6-standard.json) | 10 |
| Fortnite - Experimental | [`presets/fortnite/sb-preset-fortnite-experimental.json`](presets/fortnite/sb-preset-fortnite-experimental.json) | 10 |
| Fortnite - High Detail | [`presets/fortnite/sb-preset-fortnite-high-detail.json`](presets/fortnite/sb-preset-fortnite-high-detail.json) | 10 |
| Fortnite - Performance | [`presets/fortnite/sb-preset-fortnite-performance.json`](presets/fortnite/sb-preset-fortnite-performance.json) | 10 |
| Fortnite - Standard | [`presets/fortnite/sb-preset-fortnite-standard.json`](presets/fortnite/sb-preset-fortnite-standard.json) | 10 |
| Minecraft - Experimental | [`presets/minecraft/sb-preset-minecraft-experimental.json`](presets/minecraft/sb-preset-minecraft-experimental.json) | 10 |
| Minecraft - High Detail | [`presets/minecraft/sb-preset-minecraft-high-detail.json`](presets/minecraft/sb-preset-minecraft-high-detail.json) | 10 |
| Minecraft - Performance | [`presets/minecraft/sb-preset-minecraft-performance.json`](presets/minecraft/sb-preset-minecraft-performance.json) | 10 |
| Minecraft - Standard | [`presets/minecraft/sb-preset-minecraft-standard.json`](presets/minecraft/sb-preset-minecraft-standard.json) | 10 |
| World of Warcraft - Experimental | [`presets/world-of-warcraft/sb-preset-world-of-warcraft-experimental.json`](presets/world-of-warcraft/sb-preset-world-of-warcraft-experimental.json) | 10 |
| World of Warcraft - High Detail | [`presets/world-of-warcraft/sb-preset-world-of-warcraft-high-detail.json`](presets/world-of-warcraft/sb-preset-world-of-warcraft-high-detail.json) | 10 |
| World of Warcraft - Performance | [`presets/world-of-warcraft/sb-preset-world-of-warcraft-performance.json`](presets/world-of-warcraft/sb-preset-world-of-warcraft-performance.json) | 10 |
| World of Warcraft - Standard | [`presets/world-of-warcraft/sb-preset-world-of-warcraft-standard.json`](presets/world-of-warcraft/sb-preset-world-of-warcraft-standard.json) | 10 |
<!-- PRESETS:END -->

More games are coming. **PRs very welcome** — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Available scents

<!-- SCENTS:START -->
**25 ScentPods**
<!-- SCENTS:END --> are referenced. The full catalogue with descriptions, colors and
categories lives in [`scents.json`](scents.json) — that's also the source of
truth for the validator.

## Preset format (short version)

```json
{
  "version": 1,
  "key": "custom-<slug>",
  "name": "<Game Title>",
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
`scents.json`, and **every slot needs at least 4 unique labels**. Full spec in
[CONTRIBUTING.md](CONTRIBUTING.md) and
[`schemas/preset-schema.json`](schemas/preset-schema.json).

## Repository layout

```
presets/                  # one folder per game, one or more profiles each
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
