# Contributing

Thanks for helping build the ScentBar community preset library! 🌿

## Quick start

1. **Fork** this repo
2. Copy an existing file in [`presets/`](presets/) as a template
3. Rename it `sb-preset-<your-game-slug>.json`
4. Fill in the fields (see schema below)
5. Run the validator locally: `python scripts/validate_presets.py`
6. Open a Pull Request — the CI will validate again automatically

## Preset format

Every preset is a single JSON file matching
[`schemas/preset-schema.json`](schemas/preset-schema.json).

```json
{
  "version": 1,
  "key": "custom-<slug>",
  "name": "<Game Title>",
  "global": {
    "intensity": 4,
    "threshold": 75,
    "dutyPercent": 100,
    "cooldown": 8
  },
  "slots": [
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

### Rules

| Field | Rule |
|-------|------|
| `version` | always `1` |
| `key` | `custom-<slug>`, lowercase, hyphens, unique across the repo |
| `name` | official game title |
| `global.*` | see ranges below |
| `slots` | at least one slot |
| `slots[].value` | must exist in [`scents.json`](scents.json) |
| `slots[].display` | must match the scent's `name` from `scents.json` |
| `slots[].labels` | **minimum 3 unique labels**, lowercase preferred |
| `slots[].color` | `#RRGGBB` hex |

### Numeric ranges

| Field | Range |
|-------|-------|
| `intensity` | 1–10 |
| `threshold` | 0–100 |
| `dutyPercent` | 1–100 |
| `cooldown` | ≥ 1 second |

## Choosing labels

Labels are the keywords the ScentBar's AI vision uses to detect scenes.
Pick what is **visually obvious** in the game, not the lore. Examples:

- ✅ `gunpowder`, `explosion`, `muzzle flash`
- ✅ `desert`, `sand`, `dunes`
- ❌ `feels intense`, `enemy team` (too abstract / not visual)
- ❌ `Flying` for a Health slot (no semantic link)

Avoid duplicates and stick to one language (English is preferred so the
underlying vision model performs consistently).

## Local validation

```bash
pip install jsonschema
python scripts/validate_presets.py
```

The script checks JSON syntax, schema compliance, scent references, and
duplicate/empty labels. Same checks run in CI.

## Bundle file

`all-presets.json` is **auto-generated** on every merge to `main` by
[`build-bundle.yml`](.github/workflows/build-bundle.yml). Don't edit it
by hand.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).

## License

By submitting a preset you agree to license it under the repository's
[MIT license](LICENSE).
