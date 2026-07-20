---
layout: page
title: Products
permalink: /products/
nav: true
nav_order: 3
description: Software, apps, datasets, and models from the Baskar Group.
---

<p>Software, apps, datasets, and models from the group, cross-linked to research themes and papers.</p>

{% assign types = "software,app,model,service,dataset" | split: "," %}
{% assign labels = "Software|Apps|Models|Services|Datasets" | split: "|" %}
{% for t in types %}
  {% assign items = site.products | where: "type", t | sort: "title" %}
  {% if items.size > 0 %}
<h2 class="prod-type">{{ labels[forloop.index0] }}</h2>
<div class="product-grid">
{% for p in items %}
  <div class="product-card">
    <div class="product-head"><span class="product-title">{{ p.title }}</span><span class="product-status status-{{ p.status }}">{{ p.status }}</span></div>
    <p class="product-blurb">{{ p.blurb }}</p>
    {% if p.themes.size > 0 %}<div class="product-themes">{% for th in p.themes %}<a class="theme-chip" href="{{ '/research/#' | append: th | relative_url }}">{{ th }}</a>{% endfor %}</div>{% endif %}
    <div class="product-links">
      {% if p.links.repo %}<a href="{{ p.links.repo }}">Repo</a>{% endif %}
      {% if p.links.docs %}<a href="{{ p.links.docs }}">Docs</a>{% endif %}
      {% if p.links.app %}<a href="{{ p.links.app }}">App</a>{% endif %}
      {% if p.links.data %}<a href="{{ p.links.data }}">Data</a>{% endif %}
    </div>
  </div>
{% endfor %}
</div>
  {% endif %}
{% endfor %}

<p class="prod-note">TODO(baskar): repository and documentation links, images, and related papers for each product.</p>

<style>
  .prod-type { margin-top: 2rem; }
  .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; }
  .product-card { border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 8px; padding: .9rem 1rem; }
  .product-head { display: flex; align-items: baseline; justify-content: space-between; gap: .5rem; }
  .product-title { font-weight: 700; }
  .product-status { font-size: .7rem; text-transform: uppercase; letter-spacing: .03em; color: var(--global-text-color-light, #828282); }
  .status-active { color: #2e7d32; }
  .product-blurb { font-size: .88rem; margin: .4rem 0; }
  .product-themes { display: flex; flex-wrap: wrap; gap: .35rem; margin-bottom: .5rem; }
  .theme-chip { border: 1px solid var(--global-theme-color, #b31b1b); color: var(--global-theme-color, #b31b1b); border-radius: 999px; padding: .05rem .55rem; font-size: .72rem; text-decoration: none; }
  .product-links a { font-size: .82rem; margin-right: .7rem; }
  .prod-note { margin-top: 2rem; font-size: .85rem; color: var(--global-text-color-light, #828282); }
</style>
