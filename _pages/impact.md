---
layout: page
title: Impact
permalink: /impact/
nav: true
nav_order: 5
description: How the group's work reaches growers, industry, students, and the public.
---

Our research does not stay in journals. We turn computational advances into tools, datasets, and discoveries that reach growers, engineers, materials scientists, and the public. Baskar Ganapathysubramanian directs the [AI Institute for Resilient Agriculture (AIIRA)](https://aiira.iastate.edu/) and is Associate Director of the [Translational AI Center (TrAC)](https://trac-ai.iastate.edu/), and has been invited into national conversations on AI for science, including engagements connected to the White House Office of Science and Technology Policy and the National AI Research Resource (NAIRR).

<div class="stats-strip">
{% for s in site.data.stats %}
  <div class="stat">
    <div class="stat-value">{{ s.value }}</div>
    <div class="stat-label">{{ s.label }}</div>
    {% if s.note %}<div class="stat-note">{{ s.note }}</div>{% endif %}
  </div>
{% endfor %}
</div>

## Where the work makes a difference

**Resilient agriculture.** The group helped show that deep learning for crops can be made interpretable and trustworthy, work that helped launch AI-augmented plant science and now anchors the AIIRA institute. Group [tools, models, and benchmarks](/products/) bring insect, weed, and crop-stress identification from images to growers and researchers.

**Water and clean energy.** Computational modeling revealed that nanoscale structure improves water transport in desalination membranes, published in Science, and the group's pipelines link the nanostructure of organic solar cells to their performance.

**Materials by computation.** Graph-based methods and fast virtual instruments turn hard-to-read microscopy and X-ray data into actionable design information, letting experimentalists ask sharper questions and get quantitative answers.

**Simulation at scale.** New high-performance methods solve complex-geometry flow, heat transfer, and time-dependent problems on leadership-class supercomputers, from soft-matter manufacturing to the airflow inside buildings.

**Training the AI workforce.** More than fifty PhD and MS graduates have gone on to national laboratories (NASA, Argonne, ORNL, PNNL), to industry (Bayer, John Deere, Corning, Micron, Intel), and to faculty positions worldwide. See the [alumni wall](/people/).

<div class="impact-cta">
  <h3>Let's build what comes next</h3>
  <p>We have bold new plans taking shape. If you are a <strong>policy maker</strong> or a <strong>philanthropic partner</strong>, we would welcome a conversation, whether about the work described here or where we intend to take it next. Please <a href="mailto:{{ 'baskarg@iastate.edu' | encode_email }}?subject=Connecting%20with%20the%20Baskar%20Group">email Baskar Ganapathysubramanian</a> to start the discussion.</p>
</div>

## Funding and support

Our research is made possible by the generous support of federal, state, institutional, and industry sponsors.

<div class="funding">
{% for group in site.data.funding %}
  <div class="funding-group">
    <div class="funding-cat">{{ group.category }}</div>
    <ul class="funding-list">
      {% for f in group.funders %}
      <li class="funding-item">
        {% if f.logo %}<img class="funding-logo" src="{{ f.logo | relative_url }}" alt="{{ f.name }}" loading="lazy">
        {% elsif f.url %}<a href="{{ f.url }}" target="_blank" rel="noopener">{{ f.name }}</a>
        {% else %}{{ f.name }}{% endif %}
      </li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
</div>

<style>
  .stats-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0 2rem; }
  .stat { border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 10px; padding: 1rem; text-align: center; }
  .stat-value { font-size: 1.9rem; font-weight: 800; color: var(--global-highlight, #0e7490); line-height: 1.1; }
  .stat-label { font-size: .82rem; margin-top: .3rem; }
  .stat-note { font-size: .75rem; color: var(--global-text-color-light, #828282); margin-top: .2rem; }
  .impact-cta { border: 1px solid var(--global-divider-color, #e0e0e0); border-left: 4px solid var(--global-highlight, #0e7490); border-radius: 8px; padding: 1.1rem 1.3rem; margin: 2rem 0 1rem; background: rgba(14, 116, 144, .05); }
  .impact-cta h3 { margin: 0 0 .4rem; font-size: 1.2rem; }
  .impact-cta p { margin: 0; }
  .funding { margin: 1rem 0 1.5rem; }
  .funding-group { display: grid; grid-template-columns: 10rem 1fr; gap: .75rem 1rem; align-items: start; padding: .7rem 0; border-top: 1px solid var(--global-divider-color, #e0e0e0); }
  .funding-group:first-child { border-top: none; }
  .funding-cat { font-size: .78rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--global-text-color-light, #828282); padding-top: .2rem; }
  .funding-list { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: .45rem; }
  .funding-item { border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 999px; padding: .28rem .7rem; font-size: .85rem; line-height: 1.3; }
  .funding-item a { text-decoration: none; color: inherit; }
  .funding-item a:hover { color: var(--global-theme-color, #0e7490); }
  .funding-logo { height: 1.4rem; width: auto; display: block; }
  @media (max-width: 576px) { .funding-group { grid-template-columns: 1fr; gap: .4rem; } }
</style>
