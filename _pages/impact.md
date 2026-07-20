---
layout: page
title: Impact
permalink: /impact/
nav: true
nav_order: 5
description: How the group's work reaches growers, industry, students, and the public.
---

Our research does not stay in journals. We build tools that growers, engineers, and educators can use, we release open datasets and software, and we train the people who carry this work into national laboratories, industry, and academia. Baskar Ganapathysubramanian directs the [AI Institute for Resilient Agriculture (AIIRA)](https://aiira.iastate.edu/), a national AI institute working to make American agriculture more productive and resilient, and is Associate Director of the [Translational AI Center (TrAC)](https://trac-ai.iastate.edu/) at Iowa State University.

<div class="stats-strip">
{% for s in site.data.stats %}
  <div class="stat">
    <div class="stat-value">{{ s.value }}</div>
    <div class="stat-label">{{ s.label }}</div>
    {% if s.note %}<div class="stat-note">{{ s.note }}</div>{% endif %}
  </div>
{% endfor %}
</div>

## How the work reaches people

**Tools in growers' hands.** Products like [InsectID and WeedID](/products/) identify insects and weeds from ordinary photos, and datasets such as BioTrove and MaizeField3D give the wider research community the raw material to build their own tools.

**Open science.** The group releases software and curated datasets openly, so that other researchers, companies, and agencies can build on the work rather than repeat it.

**Training the AI workforce.** More than fifty PhD and MS graduates have gone on to national laboratories (NASA, Argonne, ORNL, PNNL), to industry (Bayer, John Deere, Corning, Micron, Intel), and to faculty positions worldwide. See the [alumni wall](/people/).

<p class="impact-todo">TODO(baskar): specific reach numbers (growers, acres, people reached) and two or three full impact stories with a hero image each.</p>

<style>
  .stats-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0 2rem; }
  .stat { border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 10px; padding: 1rem; text-align: center; }
  .stat-value { font-size: 1.9rem; font-weight: 800; color: var(--global-theme-color, #b31b1b); line-height: 1.1; }
  .stat-label { font-size: .82rem; margin-top: .3rem; }
  .stat-note { font-size: .72rem; color: var(--global-text-color-light, #828282); margin-top: .2rem; }
  .impact-todo { margin-top: 1.5rem; font-size: .85rem; color: var(--global-text-color-light, #828282); }
</style>
