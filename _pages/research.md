---
layout: page
title: Research
permalink: /research/
nav: true
nav_order: 1
description: Research themes of the Baskar Group.
---

<p>The group works across the following themes. Each theme links to the papers, products, and people associated with it (wired up in later phases).</p>

<div class="research-themes">
{% for theme in site.data.themes %}
  <section id="{{ theme.slug }}">
    <h2>{{ theme.name }}</h2>
    <p>{{ theme.blurb }}</p>
  </section>
{% endfor %}
</div>
