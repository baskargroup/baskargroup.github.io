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
  .pf-chip { border: 1px solid var(--global-theme-color, #0e7490); background: transparent; color: var(--global-theme-color, #0e7490); border-radius: 999px; padding: .15rem .7rem; font-size: .8rem; cursor: pointer; }
  .pf-chip.active { background: var(--global-theme-color, #0e7490); color: var(--global-on-accent, #fff); }
  .pf-member-banner { margin: 1rem 0 .25rem; padding: .55rem .85rem; border-radius: 8px; background: var(--global-accent-tint, #f8ecd9); border: 1px solid var(--global-divider-color, #e0e0e0); font-size: .9rem; }
  .pf-member-banner a.pf-clear-member { color: var(--global-accent-text, #b45309); font-weight: 600; text-decoration: underline; }
  @media (max-width: 576px) {
    .pub-filter { flex-direction: column; align-items: stretch; }
    .pub-filter label { display: flex; justify-content: space-between; align-items: center; }
    .pub-filter .pf-search input { min-width: 0; width: 100%; }
    .pub-filter select, .pub-filter input { min-height: 40px; padding: .45rem .5rem; }
    .pf-chip { min-height: 36px; padding: .35rem .8rem; }
    .pf-themes { gap: .55rem; }
  }
</style>
