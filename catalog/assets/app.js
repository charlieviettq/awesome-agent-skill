/* SkillHub Marketplace — recommend engine + browse + preview */

const SYNONYM_MAP = {
  tdd: ["test", "tests"],
  spec: ["requirements", "design"],
  rag: ["retrieval", "embeddings"],
  debug: ["investigate", "fix", "bug"],
  ci: ["test", "pipeline", "github"],
  pr: ["review", "pull", "merge"],
  pdf: ["document", "docx", "summarize"],
  summarize: ["pdf", "document", "summary"],
  analyze: ["pdf", "analysis", "document"],
  document: ["pdf", "docx"],
  deploy: ["ship", "release", "launch"],
  monitor: ["observability", "slo", "alert"],
};

const FIELD_WEIGHTS = [
  ["id", 18],
  ["name", 15],
  ["domain", 8],
  ["description", 8],
  ["summary", 6],
];

const REPO = "charlieviettq/awesome-agent-skill";

function expandTokens(query) {
  const raw = query.toLowerCase().split(/[^\w]+/).filter((t) => t.length > 2);
  const tokens = raw.length ? raw : [query.toLowerCase()];
  const out = [];
  for (const t of tokens) {
    out.push(t);
    (SYNONYM_MAP[t] || []).forEach((s) => out.push(s));
  }
  return out;
}

function scoreMatch(query, skill) {
  let score = 0;
  for (const token of expandTokens(query)) {
    for (const [field, weight] of FIELD_WEIGHTS) {
      const val = String(skill[field] || "").toLowerCase();
      if (val.includes(token)) score += weight;
    }
    (skill.tags || []).forEach((tag) => {
      if (String(tag).toLowerCase().includes(token)) score += 5;
    });
    (skill.triggers || []).forEach((tr) => {
      if (String(tr).toLowerCase().includes(token)) score += 10;
    });
    (skill.trigger_phrases || []).forEach((tr) => {
      if (String(tr).toLowerCase().includes(token)) score += 10;
    });
  }
  if (skill.tier === "core") score += 5;
  if (skill.risk === "low") score += 2;
  if (skill.risk === "high") score -= 3;
  const qLower = query.toLowerCase();
  const sid = String(skill.id || "").toLowerCase();
  if (qLower.includes("pdf") && sid.includes("pdf")) score += 20;
  if (qLower.includes("document") && /pdf|docx|writing-docs/.test(sid)) score += 8;
  return score;
}

function rankSkills(skills, query) {
  return skills
    .map((s) => [scoreMatch(query, s), s])
    .filter(([sc]) => sc > 0)
    .sort((a, b) => b[0] - a[0] || a[1].id.localeCompare(b[1].id));
}

function matchReasons(query, skill) {
  const reasons = [];
  for (const token of expandTokens(query)) {
    for (const [field] of FIELD_WEIGHTS) {
      if (String(skill[field] || "").toLowerCase().includes(token)) {
        reasons.push(`matched ${field}`);
        break;
      }
    }
    [...(skill.triggers || []), ...(skill.trigger_phrases || [])].forEach((tr) => {
      if (String(tr).toLowerCase().includes(token)) reasons.push(`trigger: ${tr}`);
    });
    (skill.tags || []).forEach((tag) => {
      if (String(tag).toLowerCase().includes(token)) reasons.push(`tag: ${tag}`);
    });
  }
  return [...new Set(reasons)].slice(0, 4);
}

function suggestBundle(ranked, bundles, limit = 5) {
  if (!ranked.length) return null;
  const topIds = new Set(ranked.slice(0, limit).map(([, s]) => s.id));
  const topDomains = new Set(ranked.slice(0, limit).map(([, s]) => s.domain));
  let best = null;
  for (const bundle of bundles) {
    if (bundle.id === "full") continue;
    let score = 0;
    (bundle.skills || []).forEach((sid) => {
      if (topIds.has(sid)) score += 3;
    });
    (bundle.domains || []).forEach((d) => {
      if (topDomains.has(d)) score += 2;
    });
    if (score > 0 && (!best || score > best.score)) best = { score, bundle };
  }
  return best ? best.bundle : null;
}

function installSkillCmd(id, fmt) {
  return `python3 scripts/skillhub.py install ${id} . --format ${fmt}`;
}

function installBundleCmd(id, fmt) {
  return `python3 scripts/skillhub.py install-bundle ${id} . --format ${fmt}`;
}

function fullWorkflow(bundleId, skillId, fmt) {
  const cmd = bundleId ? installBundleCmd(bundleId, fmt) : installSkillCmd(skillId, fmt);
  return `git clone https://github.com/${REPO}.git && cd awesome-agent-skill && ${cmd}`;
}

function skillGithubUrl(id) {
  return `https://github.com/${REPO}/blob/main/.cursor/skills/${id}/SKILL.md`;
}

function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const prev = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => {
      btn.textContent = prev;
    }, 1200);
  });
}

function renderCommandBox(container, command, label) {
  const wrap = document.createElement("div");
  wrap.innerHTML = `<div class="sub" style="margin:0.5rem 0 0.25rem">${label}</div>`;
  const box = document.createElement("div");
  box.className = "command-box";
  box.textContent = command;
  const btn = document.createElement("button");
  btn.className = "btn btn-small btn-secondary";
  btn.textContent = "Copy";
  btn.onclick = () => copyText(command, btn);
  box.appendChild(btn);
  wrap.appendChild(box);
  container.appendChild(wrap);
}

function normalizeSkillMarkdown(raw) {
  if (!raw) return "";
  let text = String(raw);

  // Strip front-matter if present.
  if (text.startsWith("---\n")) {
    const idx = text.indexOf("\n---", 4);
    if (idx !== -1) {
      text = text.slice(idx + 4);
    }
  }

  const hasHeading = /^#{1,6}\s/m.test(text);
  const lines = text.split("\n").filter((ln) => ln.trim().length > 0);
  const yamlLike =
    !hasHeading &&
    lines.length > 0 &&
    lines.every((ln) => /^[\w\.\-]+\s*:/.test(ln.trim()));

  if (yamlLike) {
    return "```yaml\n" + text.trim() + "\n```";
  }
  return text;
}

function initSkillModal(skillContent, agentFmt) {
  const modal = document.getElementById("skill-modal");
  const titleEl = document.getElementById("modal-title");
  const metaEl = document.getElementById("modal-meta");
  const bodyEl = document.getElementById("modal-body");
  const copyBtn = document.getElementById("modal-copy-install");
  const githubLink = document.getElementById("modal-github");
  let lastFocus = null;

  function closeModal() {
    modal.hidden = true;
    document.body.classList.remove("modal-open");
    if (lastFocus) lastFocus.focus();
  }

  function openPreview(skillId, skillMeta) {
    const entry = skillContent[skillId];
    const meta = skillMeta || {};
    lastFocus = document.activeElement;
    titleEl.textContent = entry?.name || meta.name || skillId;
    metaEl.textContent = [skillId, meta.domain, meta.tier, meta.risk && `${meta.risk} risk`]
      .filter(Boolean)
      .join(" · ");
    githubLink.href = skillGithubUrl(skillId);
    const cmd = installSkillCmd(skillId, agentFmt());
    copyBtn.onclick = () => copyText(cmd, copyBtn);
    if (entry && entry.markdown) {
      const normalized = normalizeSkillMarkdown(entry.markdown);
      if (typeof marked !== "undefined") {
        bodyEl.innerHTML = marked.parse(normalized);
      } else {
        bodyEl.innerHTML = `<pre>${escapeHtml(normalized)}</pre>`;
      }
    } else if (entry && entry.markdown) {
      bodyEl.innerHTML = `<pre>${escapeHtml(entry.markdown)}</pre>`;
    } else {
      bodyEl.innerHTML =
        '<p class="sub">Preview not available. Open SKILL.md on GitHub.</p>';
    }
    modal.hidden = false;
    document.body.classList.add("modal-open");
    modal.querySelector(".modal-close").focus();
  }

  modal.querySelectorAll("[data-close-modal]").forEach((el) => {
    el.addEventListener("click", closeModal);
  });

  document.addEventListener("keydown", (e) => {
    if (!modal.hidden && e.key === "Escape") closeModal();
  });

  return { openPreview, closeModal };
}

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
function initMarketplace(skills, bundles, quality, skillContent) {
  const params = new URLSearchParams(location.search);
  let domainFilter = params.get("domain") || "";
  let bundleFilter = params.get("bundle") || "";
  let tierFilter = params.get("tier") || "";
  let riskFilter = params.get("risk") || "";
  let agentFilter = params.get("agent") || "cursor";
  let minQuality = parseInt(params.get("minQ") || "0", 10) || 0;

  const qInput = document.getElementById("q");
  const taskInput = document.getElementById("task");
  const agentSelect = document.getElementById("agent");
  const list = document.getElementById("list");
  const domainsEl = document.getElementById("domains");
  const bundlesFilterEl = document.getElementById("bundles-filter");
  const tierEl = document.getElementById("tiers");
  const riskEl = document.getElementById("risks");
  const qualityEl = document.getElementById("quality-filter");
  const bundleGrid = document.getElementById("bundle-grid");
  const countEl = document.getElementById("shown-count");
  const advisorResult = document.getElementById("advisor-result");
  const activeFiltersWrap = document.getElementById("active-filters");
  const activeFilterChips = document.getElementById("active-filter-chips");

  const modalApi = initSkillModal(skillContent, () => agentSelect.value);

  if (params.get("task")) taskInput.value = params.get("task");
  if (params.get("q")) qInput.value = params.get("q");
  agentSelect.value = agentFilter;

  function bundleSkillIds(bundle) {
    const ids = new Set(bundle.skills || []);
    if (bundle.domains) {
      skills.forEach((s) => {
        if (bundle.domains.includes(s.domain)) ids.add(s.id);
      });
    }
    return ids;
  }

  function applyBundleFilter(bundleId) {
    bundleFilter = bundleId;
    domainFilter = "";
    renderFilters();
    renderSkills();
    updateActiveFilters();
    document.getElementById("skills-section").scrollIntoView({ behavior: "smooth" });
  }

  function applyDomainFilter(domain) {
    domainFilter = domain;
    bundleFilter = "";
    renderFilters();
    renderSkills();
    updateActiveFilters();
    document.getElementById("skills-section").scrollIntoView({ behavior: "smooth" });
  }

  function applySkillFilter(skillId) {
    qInput.value = skillId.split("/").pop();
    renderSkills();
    updateActiveFilters();
    document.getElementById("skills-section").scrollIntoView({ behavior: "smooth" });
  }

  if (typeof SkillHubGraph !== "undefined") {
    SkillHubGraph.initBundleGraph(
      document.getElementById("graph-container"),
      skills,
      bundles,
      {
        onBundle: applyBundleFilter,
        onDomain: applyDomainFilter,
        onSkill: (id) => modalApi.openPreview(id, skills.find((s) => s.id === id)),
      }
    );
  }

  function renderBundles() {
    bundleGrid.innerHTML = bundles
      .filter((b) => b.id !== "full")
      .map(
        (b) => `
      <article class="bundle-card glass" data-bundle="${b.id}">
        <h3>${b.title}</h3>
        <p>${b.description || ""}</p>
        <div class="badges"><span class="badge">~${bundleSkillCount(b)} skills</span></div>
        <div class="card-actions">
          <button class="btn btn-small" data-install-bundle="${b.id}">Copy install</button>
          <button class="btn btn-small btn-secondary" data-filter-bundle="${b.id}">Browse</button>
        </div>
      </article>`
      )
      .join("");

    bundleGrid.querySelectorAll("[data-install-bundle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        copyText(installBundleCmd(btn.dataset.installBundle, agentSelect.value), btn);
      });
    });
    bundleGrid.querySelectorAll("[data-filter-bundle]").forEach((btn) => {
      btn.addEventListener("click", () => applyBundleFilter(btn.dataset.filterBundle));
    });
  }

  function bundleSkillCount(bundle) {
    if (bundle.install_all_domains) return skills.length;
    let n = (bundle.skills || []).length;
    (bundle.domains || []).forEach((d) => {
      n += skills.filter((s) => s.domain === d).length;
    });
    return n;
  }

  function renderFilters() {
    const mk = (el, items, current, key, allLabel) => {
      el.innerHTML = "";
      const all = document.createElement("button");
      all.type = "button";
      all.className = `chip${current ? "" : " active"}`;
      all.textContent = allLabel;
      all.onclick = () => {
        if (key === "domain") domainFilter = "";
        if (key === "tier") tierFilter = "";
        if (key === "risk") riskFilter = "";
        if (key === "bundle") bundleFilter = "";
        if (key === "quality") minQuality = 0;
        renderFilters();
        renderSkills();
        updateActiveFilters();
      };
      el.appendChild(all);
      items.forEach((item) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = `chip${current === item ? " active" : ""}`;
        b.textContent = typeof item === "number" ? `Q${item}+` : item;
        b.onclick = () => {
          if (key === "domain") {
            domainFilter = item;
            bundleFilter = "";
          }
          if (key === "tier") tierFilter = item;
          if (key === "risk") riskFilter = item;
          if (key === "bundle") {
            bundleFilter = item;
            domainFilter = "";
          }
          if (key === "quality") minQuality = item;
          renderFilters();
          renderSkills();
          updateActiveFilters();
        };
        el.appendChild(b);
      });
    };

    mk(
      bundlesFilterEl,
      bundles.filter((b) => b.id !== "full").map((b) => b.id),
      bundleFilter,
      "bundle",
      "All bundles"
    );
    mk(
      domainsEl,
      [...new Set(skills.map((s) => s.domain))].sort(),
      domainFilter,
      "domain",
      "All domains"
    );
    mk(tierEl, ["core", "extended"], tierFilter, "tier", "All tiers");
    mk(riskEl, ["low", "medium", "high"], riskFilter, "risk", "All risk");
    mk(qualityEl, [50, 70, 85], minQuality, "quality", "Any");
  }

  function updateActiveFilters() {
    const active = [];
    if (bundleFilter) active.push({ label: `bundle: ${bundleFilter}`, clear: () => { bundleFilter = ""; } });
    if (domainFilter) active.push({ label: `domain: ${domainFilter}`, clear: () => { domainFilter = ""; } });
    if (tierFilter) active.push({ label: `tier: ${tierFilter}`, clear: () => { tierFilter = ""; } });
    if (riskFilter) active.push({ label: `risk: ${riskFilter}`, clear: () => { riskFilter = ""; } });
    if (minQuality) active.push({ label: `Q${minQuality}+`, clear: () => { minQuality = 0; } });
    if (qInput.value.trim()) active.push({ label: `search: ${qInput.value.trim()}`, clear: () => { qInput.value = ""; } });

    if (!active.length) {
      activeFiltersWrap.hidden = true;
      return;
    }
    activeFiltersWrap.hidden = false;
    activeFilterChips.innerHTML = "";
    active.forEach((a) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip active filter-removable";
      chip.textContent = `${a.label} ×`;
      chip.onclick = () => {
        a.clear();
        renderFilters();
        renderSkills();
        updateActiveFilters();
      };
      activeFilterChips.appendChild(chip);
    });
  }

  document.getElementById("clear-filters").addEventListener("click", () => {
    domainFilter = "";
    bundleFilter = "";
    tierFilter = "";
    riskFilter = "";
    minQuality = 0;
    qInput.value = "";
    renderFilters();
    renderSkills();
    updateActiveFilters();
  });

  function passesFilters(s) {
    if (domainFilter && s.domain !== domainFilter) return false;
    if (tierFilter && s.tier !== tierFilter) return false;
    if (riskFilter && s.risk !== riskFilter) return false;
    if (minQuality && (quality[s.id] || 0) < minQuality) return false;
    if (bundleFilter) {
      const bundle = bundles.find((b) => b.id === bundleFilter);
      if (bundle && !bundleSkillIds(bundle).has(s.id)) return false;
    }
    if (agentFilter === "cursor" && !(s.formats || []).includes("cursor")) return false;
    if (agentFilter === "claude" && !(s.formats || []).includes("claude")) return false;
    const term = (qInput.value || "").toLowerCase();
    if (!term) return true;
    const blob = [s.id, s.name, s.domain, s.description, ...(s.tags || []), ...(s.triggers || [])]
      .join(" ")
      .toLowerCase();
    return blob.includes(term);
  }

  function renderSkills() {
    const filtered = skills.filter(passesFilters);
    countEl.textContent = `${filtered.length} / ${skills.length}`;
    if (!filtered.length) {
      list.innerHTML = '<div class="empty">No skills match your filters.</div>';
      return;
    }
    list.innerHTML = filtered
      .map((s) => {
        const qsc = quality[s.id];
        const qBadge = qsc != null ? `<span class="badge q">Q${qsc}</span>` : "";
        const tierBadge = s.tier ? `<span class="badge ${s.tier}">${s.tier}</span>` : "";
        const riskBadge = s.risk ? `<span class="badge ${s.risk}">${s.risk} risk</span>` : "";
        const tags = (s.tags || [])
          .slice(0, 3)
          .map((t) => `<span class="badge">${t}</span>`)
          .join("");
        const installCmd = installSkillCmd(s.id, agentSelect.value);
        const hasPreview = !!skillContent[s.id];
        return `
        <article class="skill-card glass">
          <header>
            <div>
              <h3>${s.name}</h3>
              <div class="skill-id">${s.id}</div>
            </div>
            <div class="badges">${qBadge}${tierBadge}${riskBadge}</div>
          </header>
          <div class="badges">${tags}</div>
          <p>${(s.description || "").replace(/^>\s*/gm, "").slice(0, 180)}</p>
          <div class="card-actions">
            ${
              hasPreview
                ? `<button class="btn btn-small" data-preview="${s.id}">Preview skill</button>`
                : ""
            }
            <button class="btn btn-small btn-secondary" data-copy="${encodeURIComponent(
              installCmd
            )}">Copy install</button>
            <a class="btn btn-small btn-secondary" href="${skillGithubUrl(
              s.id
            )}" target="_blank" rel="noopener">GitHub</a>
          </div>
        </article>`;
      })
      .join("");

    list.querySelectorAll("[data-copy]").forEach((btn) => {
      btn.addEventListener("click", () => copyText(decodeURIComponent(btn.dataset.copy), btn));
    });
    list.querySelectorAll("[data-preview]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const skill = skills.find((s) => s.id === btn.dataset.preview);
        modalApi.openPreview(btn.dataset.preview, skill);
      });
    });
  }

  function runAdvisor() {
    const query = (taskInput.value || "").trim();
    if (!query) return;
    const ranked = rankSkills(skills, query);
    const bundle = suggestBundle(ranked, bundles);
    const fmt = agentSelect.value;
    advisorResult.innerHTML = "";
    advisorResult.classList.add("visible");

    if (!ranked.length) {
      advisorResult.innerHTML = '<div class="empty">No matching skills. Try different wording.</div>';
      return;
    }

    if (bundle) {
      const box = document.createElement("div");
      box.className = "advisor-bundle";
      box.innerHTML = `<strong>Recommended bundle:</strong> ${bundle.title}<br><span style="color:var(--text-muted)">${bundle.description || ""}</span>`;
      advisorResult.appendChild(box);
      renderCommandBox(advisorResult, fullWorkflow(bundle.id, null, fmt), "Full install workflow");
      renderCommandBox(advisorResult, installBundleCmd(bundle.id, fmt), "From repo root");
    }

    const ul = document.createElement("ul");
    ul.className = "rec-list";
    ranked.slice(0, 5).forEach(([sc, s]) => {
      const reasons = matchReasons(query, s).join(" · ");
      const li = document.createElement("li");
      li.innerHTML = `<strong>${s.name}</strong> <span class="skill-id">(${s.id})</span> — score ${sc}<br><span style="color:var(--text-muted);font-size:0.85rem">${reasons}</span>`;
      if (skillContent[s.id]) {
        const pb = document.createElement("button");
        pb.className = "btn btn-small btn-secondary";
        pb.style.marginTop = "0.35rem";
        pb.textContent = "Preview";
        pb.onclick = () => modalApi.openPreview(s.id, s);
        li.appendChild(document.createElement("br"));
        li.appendChild(pb);
      }
      ul.appendChild(li);
    });
    advisorResult.appendChild(ul);

    const note = document.createElement("p");
    note.className = "sub";
    note.textContent =
      fmt === "cursor"
        ? "Reload Cursor window or start a new chat after installing."
        : "Restart Claude Code session after installing.";
    advisorResult.appendChild(note);
  }

  qInput.addEventListener("input", () => {
    renderSkills();
    updateActiveFilters();
  });
  agentSelect.addEventListener("change", () => {
    agentFilter = agentSelect.value;
    renderSkills();
  });
  document.getElementById("run-advisor").addEventListener("click", runAdvisor);
  taskInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") runAdvisor();
  });

  if (params.get("preview")) {
    const pid = params.get("preview");
    if (skillContent[pid]) modalApi.openPreview(pid, skills.find((s) => s.id === pid));
  }

  renderBundles();
  renderFilters();
  renderSkills();
  updateActiveFilters();
  if (taskInput.value) runAdvisor();
}

async function boot() {
  const [skillsRes, bundlesRes, qualityRes, contentRes] = await Promise.all([
    fetch("data/skills.json"),
    fetch("data/bundles.json"),
    fetch("data/quality.json").catch(() => null),
    fetch("data/skill-content.json").catch(() => null),
  ]);
  const skillsPayload = await skillsRes.json();
  const bundlesPayload = await bundlesRes.json();
  let quality = {};
  let skillContent = {};
  if (qualityRes && qualityRes.ok) {
    const qdata = await qualityRes.json();
    if (Array.isArray(qdata.skills)) {
      qdata.skills.forEach((r) => {
        quality[r.id] = r.score;
      });
    } else {
      quality = qdata;
    }
  }
  if (contentRes && contentRes.ok) {
    skillContent = await contentRes.json();
  }
  initMarketplace(
    skillsPayload.skills || skillsPayload,
    bundlesPayload.bundles || bundlesPayload,
    quality,
    skillContent
  );
}

boot();
