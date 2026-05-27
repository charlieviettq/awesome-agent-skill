/* D3 force graph — bundle → domain → skill relationships */

(function (global) {
  "use strict";

  const MAX_SKILLS_PER_DOMAIN = 3;

  function buildGraphData(skills, bundles) {
    const nodes = [];
    const links = [];
    const seen = new Set();

    function addNode(id, type, label, extra) {
      if (seen.has(id)) return;
      seen.add(id);
      nodes.push({ id, type, label, ...extra });
    }

    const usable = bundles.filter((b) => b.id !== "full");
    usable.forEach((bundle) => {
      const bid = `bundle:${bundle.id}`;
      addNode(bid, "bundle", bundle.title, { bundleId: bundle.id });

      (bundle.domains || []).forEach((domain) => {
        const did = `domain:${domain}`;
        addNode(did, "domain", domain, { domain });
        links.push({ source: bid, target: did });

        const domainSkills = skills
          .filter((s) => s.domain === domain)
          .sort((a, b) => (b.tier === "core" ? 1 : 0) - (a.tier === "core" ? 1 : 0))
          .slice(0, MAX_SKILLS_PER_DOMAIN);

        domainSkills.forEach((s) => {
          const sid = `skill:${s.id}`;
          addNode(sid, "skill", s.name, { skillId: s.id });
          links.push({ source: did, target: sid });
        });
      });

      (bundle.skills || []).forEach((skillId) => {
        const skill = skills.find((s) => s.id === skillId);
        if (!skill) return;
        const sid = `skill:${skillId}`;
        addNode(sid, "skill", skill.name, { skillId });
        links.push({ source: bid, target: sid });
      });
    });

    return { nodes, links };
  }

  function initBundleGraph(container, skills, bundles, callbacks) {
    if (typeof d3 === "undefined") {
      const fb = document.getElementById("graph-fallback");
      if (fb) fb.hidden = false;
      return null;
    }

    const { nodes, links } = buildGraphData(skills, bundles);
    if (!nodes.length) return null;

    const width = container.clientWidth || 900;
    const height = Math.min(520, Math.max(360, nodes.length * 12));

    container.innerHTML = "";
    const svg = d3
      .select(container)
      .append("svg")
      .attr("viewBox", [0, 0, width, height])
      .attr("width", "100%")
      .attr("height", height)
      .attr("role", "img")
      .attr("aria-label", "Bundle domain skill graph");

    const g = svg.append("g");

    const zoom = d3
      .zoom()
      .scaleExtent([0.4, 2.5])
      .on("zoom", (event) => g.attr("transform", event.transform));
    svg.call(zoom);

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance((l) => {
            const s = l.source.type || l.source;
            const t = l.target.type || l.target;
            if (s === "bundle" || t === "bundle") return 90;
            return 55;
          })
          .strength(0.6)
      )
      .force("charge", d3.forceManyBody().strength(-280))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius((d) => radius(d) + 6));

    const link = g
      .append("g")
      .attr("class", "graph-links")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", "graph-link");

    const node = g
      .append("g")
      .attr("class", "graph-nodes")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", (d) => `graph-node graph-node-${d.type}`)
      .style("cursor", "pointer")
      .call(
        d3
          .drag()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    node
      .append("circle")
      .attr("r", (d) => radius(d))
      .attr("class", (d) => `graph-circle graph-circle-${d.type}`);

    node
      .append("text")
      .attr("class", "graph-label")
      .attr("dy", (d) => radius(d) + 14)
      .attr("text-anchor", "middle")
      .text((d) => truncate(d.label, d.type === "skill" ? 18 : 24));

    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "graph-tooltip")
      .style("opacity", 0);

    node
      .on("mouseenter", (event, d) => {
        highlight(d);
        tooltip
          .style("opacity", 1)
          .html(`<strong>${d.label}</strong><br><span>${d.type}</span>`)
          .style("left", `${event.pageX + 12}px`)
          .style("top", `${event.pageY - 8}px`);
      })
      .on("mousemove", (event) => {
        tooltip.style("left", `${event.pageX + 12}px`).style("top", `${event.pageY - 8}px`);
      })
      .on("mouseleave", () => {
        clearHighlight();
        tooltip.style("opacity", 0);
      })
      .on("click", (_, d) => {
        if (d.type === "bundle" && callbacks.onBundle) callbacks.onBundle(d.bundleId);
        if (d.type === "domain" && callbacks.onDomain) callbacks.onDomain(d.domain);
        if (d.type === "skill" && callbacks.onSkill) callbacks.onSkill(d.skillId);
      });

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);
      node.attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    function radius(d) {
      if (d.type === "bundle") return 22;
      if (d.type === "domain") return 14;
      return 8;
    }

    function truncate(s, n) {
      return s.length > n ? `${s.slice(0, n)}…` : s;
    }

    function highlight(d) {
      const connected = new Set([d.id]);
      links.forEach((l) => {
        const sid = l.source.id || l.source;
        const tid = l.target.id || l.target;
        if (sid === d.id) connected.add(tid);
        if (tid === d.id) connected.add(sid);
      });
      node.classed("dimmed", (n) => !connected.has(n.id));
      link.classed("dimmed", (l) => {
        const sid = l.source.id || l.source;
        const tid = l.target.id || l.target;
        return sid !== d.id && tid !== d.id;
      });
    }

    function clearHighlight() {
      node.classed("dimmed", false);
      link.classed("dimmed", false);
    }

    return { simulation, svg };
  }

  global.SkillHubGraph = { initBundleGraph, buildGraphData };
})(window);
