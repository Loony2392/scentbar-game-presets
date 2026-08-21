# GitHub Pages — ScentBar Game Presets

This folder contains the static landing site that ships with the repo.

## Enable GitHub Pages

1. Go to **Settings → Pages**
2. **Source:** *Deploy from a branch*
3. **Branch:** `main` · **Folder:** `/docs`
4. Save — your site goes live at:
   `https://<your-username>.github.io/scentbar-game-presets/`

## Files

| File | Purpose |
|---|---|
| `index.html` | The landing page |
| `style.css`  | Aurora / Celestia-inspired theme |
| `data.js`    | Generated fallback data for scents + presets |
| `app.js`     | Search filter and DOM rendering |
| `.nojekyll`  | Tells Pages to serve files as-is |

## Updating scents and profiles

Add scents to `scents.json`. Add profiles under a game folder in `presets/`,
for example:

```js
presets/
   game-name/
      sb-preset-game-standard.json
      sb-preset-game-performance.json
```

The Pages app loads `scents.json` and `all-presets.json` directly from the
`main` branch on every page load. The build workflow keeps the bundle and
fallback data current automatically.
