<!-- Thanks for contributing a preset! -->

## Game

- **Title:** <!-- e.g. Battlefield 6 -->
- **Filename:** `presets/sb-preset-<slug>.json`
- **Preset key:** `custom-<slug>`

## Checklist

- [ ] File is named `sb-preset-<slug>.json` and lives in `presets/`
- [ ] `version` is `1`
- [ ] `key` matches `^custom-[a-z0-9-]+$` and is unique
- [ ] `name` is the official game title
- [ ] Every slot uses a `value` from [`scents.json`](../scents.json)
- [ ] Every `display` matches the `name` from `scents.json`
- [ ] Every slot has **at least 3 unique labels** (lowercase preferred)
- [ ] All numeric ranges are valid:
  - `intensity` 1–10
  - `threshold` 0–100
  - `dutyPercent` 1–100
  - `cooldown` ≥ 1
- [ ] Tested in the ScentBar app (or marked as untested below)

## Tested?

- [ ] Yes, I ran this preset live with my ScentBar
- [ ] No, this is a community-tuned preset based on gameplay observation

## Notes

<!-- Anything reviewers should know? Genre, notable tweaks, intended scenes, etc. -->
