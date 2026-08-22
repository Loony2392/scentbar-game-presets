/* ScentBar Game Presets — landing page logic */
(() => {
  const REPO_BASE = "https://github.com/loony2392/scentbar-game-presets/blob/main/presets/";
  const RAW_PRESET_BASE = "https://raw.githubusercontent.com/loony2392/scentbar-game-presets/main/presets/";
  const DATA_BASE = "https://raw.githubusercontent.com/loony2392/scentbar-game-presets/main/";

  const scentGrid = document.getElementById("scent-grid");
  const grid = document.getElementById("preset-grid");
  const search = document.getElementById("search");
  const profileFilter = document.getElementById("profile-filter");
  const count = document.getElementById("count");
  const statPresets = document.getElementById("stat-presets");
  const statScents = document.getElementById("stat-scents");
  const scentTitleCount = document.getElementById("scent-title-count");
  const heroScentCount = document.getElementById("hero-scent-count");

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "\"":"&quot;", "'":"&#39;" }[c]));
  }

  function renderScents(scents) {
    if (!scentGrid) return;
    scentGrid.innerHTML = scents.map(s => `
      <div class="scent" title="${s.desc}">
        <div class="dot" style="background:${s.color}; color:${s.color};"></div>
        <div>
          <div class="name">${escapeHtml(s.emoji || "✨")} ${escapeHtml(s.name)}</div>
          <div class="cat">${escapeHtml(s.category)}</div>
        </div>
      </div>
    `).join("");
    if (statScents) statScents.textContent = scents.length;
    if (scentTitleCount) scentTitleCount.textContent = scents.length;
    if (heroScentCount) heroScentCount.textContent = scents.length;
  }

  function renderPresets(presets, filter = "", profile = "") {
    const q = filter.trim().toLowerCase();
    const list = presets.filter(p => {
      const matchesSearch = !q || p.game.toLowerCase().includes(q) || p.name.toLowerCase().includes(q) || p.key.toLowerCase().includes(q);
      const matchesProfile = !profile || p.profile === profile;
      return matchesSearch && matchesProfile;
    });

    if (!list.length) {
      grid.innerHTML = `<div class="empty">😢 No games matching "<b>${escapeHtml(filter)}</b>".<br><br>
        <a class="btn ghost" href="https://github.com/loony2392/scentbar-game-presets/issues/new/choose" target="_blank" rel="noopener">🎮 Request this game</a>
      </div>`;
    } else {
      const games = new Map();
      list.forEach(p => {
        if (!games.has(p.game)) games.set(p.game, []);
        games.get(p.game).push(p);
      });
      grid.innerHTML = [...games].map(([game, profiles]) => `
        <div class="preset-game">
          <h3>${escapeHtml(game)}</h3>
          <div class="profile-tags">
            ${profiles.map(p => `
              <a class="profile-tag" href="${RAW_PRESET_BASE}${p.file.split("/").map(encodeURIComponent).join("/")}" target="_blank" rel="noopener" download>
                ${escapeHtml(p.profile)}<span class="arrow">›</span>
              </a>
            `).join("")}
          </div>
        </div>
      `).join("");
    }
    if (count) count.textContent = `${list.length} of ${presets.length}`;
  }

  async function loadData() {
    const cacheBust = `?t=${Date.now()}`;
    const [scentsResponse, presetsResponse] = await Promise.all([
      fetch(`${DATA_BASE}scents.json${cacheBust}`, { cache: "no-store" }),
      fetch(`${DATA_BASE}all-presets.json${cacheBust}`, { cache: "no-store" }),
    ]);
    if (!scentsResponse.ok || !presetsResponse.ok) throw new Error("Unable to load repository data");
    const scents = (await scentsResponse.json()).scents;
    const bundle = await presetsResponse.json();
    const filesByKey = Object.fromEntries((bundle.presetFiles || []).map(item => [item.key, item.file]));
    const presets = bundle.presets.map(p => {
      const profileMatch = p.name.match(/^(.*) - (Performance|Standard|High Detail|Experimental)$/i);
      const profile = profileMatch?.[2] || "Standard";
      return {
        name: p.name,
        game: profileMatch?.[1] || p.name,
        key: p.key,
        profile,
        file: filesByKey[p.key] || `${p.key}.json`.replace(/^custom-/, "sb-preset-"),
      };
    });
    renderScents(scents);
    if (statPresets) statPresets.textContent = presets.length;
    if (grid) {
      const profiles = [...new Set(presets.map(p => p.profile))].sort();
      profileFilter.replaceChildren(
        new Option("All AI profiles", ""),
        ...profiles.map(profile => new Option(profile, profile)),
      );
      renderPresets(presets);
      search.addEventListener("input", e => renderPresets(presets, e.target.value, profileFilter.value));
      profileFilter.addEventListener("change", e => renderPresets(presets, search.value, e.target.value));
    }
  }

  loadData().catch(error => {
    console.error(error);
    if (scentGrid) scentGrid.innerHTML = `<div class="empty">Unable to load scents right now.</div>`;
    if (grid) grid.innerHTML = `<div class="empty">Unable to load presets right now.</div>`;
  });
})();
