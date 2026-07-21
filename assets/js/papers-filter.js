---
---
// Faceted publications filter (PLAN.md Section 6.4).
// Drives year + theme + free-text facets from papers.json against the
// jekyll-scholar DOM. AND semantics across facets, live count, and filter state
// synced to URL params (?year=&theme=&q=) so filtered views are shareable.
// Degrades gracefully: without JS the full list renders normally.
(function () {
  "use strict";
  var container = document.querySelector(".publications");
  if (!container) return;
  var jsonUrl = container.getAttribute("data-papers-json") || "/assets/json/papers.json";

  fetch(jsonUrl)
    .then(function (r) { return r.json(); })
    .then(function (papers) {
      var byKey = {};
      papers.forEach(function (p) { byKey[p.bibkey] = p; });

      // Each <li> holds one entry whose inner div id is the bibkey.
      var entries = [];
      container.querySelectorAll("ol.bibliography > li").forEach(function (li) {
        var idNode = li.querySelector("[id]");
        var data = idNode && byKey[idNode.id];
        if (data) entries.push({ li: li, data: data });
      });
      if (!entries.length) return;

      var groups = [];
      container.querySelectorAll("ol.bibliography").forEach(function (ol) {
        var h2 = ol.previousElementSibling;
        groups.push({ ol: ol, header: h2 && h2.tagName === "H2" ? h2 : null });
      });

      var years = {}, themes = {};
      entries.forEach(function (e) {
        if (e.data.year) years[e.data.year] = true;
        (e.data.themes || []).forEach(function (t) { themes[t] = true; });
      });
      var yearList = Object.keys(years).sort(function (a, b) { return b - a; });
      var themeList = Object.keys(themes).sort();

      var bar = document.createElement("div");
      bar.className = "pub-filter";
      bar.innerHTML =
        '<label>Year <select id="pf-year"><option value="">all</option>' +
        yearList.map(function (y) { return '<option value="' + y + '">' + y + "</option>"; }).join("") +
        "</select></label>" +
        '<label>Type <select id="pf-status">' +
        '<option value="">all</option>' +
        '<option value="published">published</option>' +
        '<option value="preprint">arXiv / preprint</option>' +
        '<option value="other">no identifier</option>' +
        "</select></label>" +
        '<label class="pf-search">Search <input type="search" id="pf-q" placeholder="title, author, summary"></label>' +
        '<span class="pf-count" id="pf-count"></span>' +
        (themeList.length
          ? '<div class="pf-themes">' +
            themeList.map(function (t) { return '<button type="button" class="pf-chip" data-theme="' + t + '">' + t + "</button>"; }).join("") +
            "</div>"
          : "");
      container.parentNode.insertBefore(bar, container);

      var yearSel = bar.querySelector("#pf-year");
      var statusSel = bar.querySelector("#pf-status");
      var qInput = bar.querySelector("#pf-q");
      var countEl = bar.querySelector("#pf-count");
      var state = { year: "", status: "", q: "", theme: "", member: "" };

      function readURL() {
        var p = new URLSearchParams(location.search);
        state.year = p.get("year") || "";
        state.status = p.get("status") || "";
        state.q = p.get("q") || "";
        state.theme = p.get("theme") || "";
        state.member = p.get("member") || "";
      }
      function writeURL() {
        var p = new URLSearchParams();
        if (state.year) p.set("year", state.year);
        if (state.status) p.set("status", state.status);
        if (state.q) p.set("q", state.q);
        if (state.theme) p.set("theme", state.theme);
        if (state.member) p.set("member", state.member);
        var qs = p.toString();
        history.replaceState(null, "", qs ? "?" + qs : location.pathname);
      }
      function matches(e) {
        if (state.year && String(e.data.year) !== state.year) return false;
        if (state.status && e.data.status !== state.status) return false;
        if (state.theme && (e.data.themes || []).indexOf(state.theme) < 0) return false;
        // member: filter by group-member slug (robust, from papers.json members)
        if (state.member && (e.data.members || []).indexOf(state.member) < 0) return false;
        if (state.q) {
          var hay = (e.data.title + " " + (e.data.authors || []).join(" ") + " " + (e.data.summary || "")).toLowerCase();
          if (hay.indexOf(state.q.toLowerCase()) < 0) return false;
        }
        return true;
      }
      function apply() {
        var shown = 0;
        entries.forEach(function (e) {
          var ok = matches(e);
          e.li.style.display = ok ? "" : "none";
          if (ok) shown++;
        });
        groups.forEach(function (g) {
          var anyVisible = g.ol.querySelector('li:not([style*="display: none"])') !== null;
          g.ol.style.display = anyVisible ? "" : "none";
          if (g.header) g.header.style.display = anyVisible ? "" : "none";
        });
        countEl.textContent = shown + " / " + entries.length + " papers";
        yearSel.value = state.year;
        statusSel.value = state.status;
        qInput.value = state.q;
        bar.querySelectorAll(".pf-chip").forEach(function (c) {
          c.classList.toggle("active", c.getAttribute("data-theme") === state.theme);
        });
        writeURL();
      }

      yearSel.addEventListener("change", function () { state.year = this.value; apply(); });
      statusSel.addEventListener("change", function () { state.status = this.value; apply(); });
      qInput.addEventListener("input", function () { state.q = this.value; apply(); });
      bar.querySelectorAll(".pf-chip").forEach(function (c) {
        c.addEventListener("click", function () {
          var t = this.getAttribute("data-theme");
          state.theme = state.theme === t ? "" : t;
          apply();
        });
      });

      readURL();
      apply();
    })
    .catch(function (err) { console.error("papers-filter:", err); });
})();
