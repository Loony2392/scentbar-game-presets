/* ScentBar Game Presets — landing page logic */
(() => {
  const REPO_BASE = "https://github.com/loony2392/scentbar-game-presets/blob/main/presets/";

  // ----- Scents -----
  const scentGrid = document.getElementById("scent-grid");
  if (scentGrid) {
    scentGrid.innerHTML = SCENTS.map(s => `
      <div class="scent" title="${s.desc}">
        <div class="dot" style="background:${s.color}; color:${s.color};"></div>
        <div>
          <div class="name">${s.emoji} ${s.name}</div>
          <div class="cat">${s.category}</div>
        </div>
      </div>
    `).join("");
  }

  // ----- Presets -----
  const grid = document.getElementById("preset-grid");
  const search = document.getElementById("search");
  const count = document.getElementById("count");
  const statPresets = document.getElementById("stat-presets");

  function render(filter = "") {
    const q = filter.trim().toLowerCase();
    const list = q
      ? PRESETS.filter(([name, file]) => name.toLowerCase().includes(q) || file.toLowerCase().includes(q))
      : PRESETS;

    if (!list.length) {
      grid.innerHTML = `<div class="empty">😢 No games matching "<b>${escapeHtml(filter)}</b>".<br><br>
        <a class="btn ghost" href="https://github.com/loony2392/scentbar-game-presets/issues/new/choose" target="_blank" rel="noopener">🎮 Request this game</a>
      </div>`;
    } else {
      grid.innerHTML = list.map(([name, file]) => `
        <a class="preset" href="${REPO_BASE}${encodeURIComponent(file)}" target="_blank" rel="noopener">
          ${escapeHtml(name)}<span class="arrow">›</span>
        </a>
      `).join("");
    }
    count.textContent = `${list.length} of ${PRESETS.length}`;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;" }[c]));
  }

  if (statPresets) statPresets.textContent = PRESETS.length;
  if (grid) {
    render();
    search.addEventListener("input", e => render(e.target.value));
  }
})();
