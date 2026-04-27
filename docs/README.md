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
| `data.js`    | Static list of scents + presets (no build step required) |
| `app.js`     | Search filter and DOM rendering |
| `.nojekyll`  | Tells Pages to serve files as-is |

## Updating the preset list

When you add a new preset under `presets/`, also add a one-liner to the
`PRESETS` array in `data.js`:

```js
["Game Display Name", "sb-preset-game-slug.json"],
```

That's it — no build, no framework, no dependencies.
