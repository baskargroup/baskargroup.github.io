---
layout: page
permalink: /publications/
title: Publications
description: Publications by the Baskar Group, in reverse chronological order.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->
<!-- Faceted filter (year, theme, text) is added by assets/js/papers-filter.js.
     Without JavaScript the full year-grouped list below renders normally. -->

<div class="publications" data-papers-json="{{ '/assets/json/papers.json' | relative_url }}">

{% bibliography %}

</div>

<script src="{{ '/assets/js/papers-filter.js' | relative_url }}"></script>

<style>
  .pub-filter { display: flex; flex-wrap: wrap; align-items: center; gap: .75rem; margin: 1rem 0 1.5rem; padding-bottom: .75rem; border-bottom: 1px solid var(--global-divider-color, #e0e0e0); }
  .pub-filter label { font-size: .9rem; }
  .pub-filter select, .pub-filter input { margin-left: .35rem; padding: .25rem .4rem; }
  .pub-filter .pf-search input { min-width: 16rem; max-width: 100%; }
  .pub-filter .pf-count { color: var(--global-text-color-light, #828282); font-size: .85rem; }
  .pub-filter .pf-themes { flex-basis: 100%; display: flex; flex-wrap: wrap; gap: .4rem; }
  .pf-chip { border: 1px solid var(--global-theme-color, #b31b1b); background: transparent; color: var(--global-theme-color, #b31b1b); border-radius: 999px; padding: .15rem .7rem; font-size: .8rem; cursor: pointer; }
  .pf-chip.active { background: var(--global-theme-color, #b31b1b); color: #fff; }
</style>
