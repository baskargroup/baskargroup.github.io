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

**Resilient agriculture.** The group helped show that deep learning for crops can be made interpretable and trustworthy, work that helped launch AI-augmented plant science and now anchors the AIIRA institute. Tools like [InsectID and WeedID](/products/) bring pest and weed identification to an ordinary phone photo.

**Water and clean energy.** Computational modeling revealed that nanoscale structure improves water transport in desalination membranes, published in Science, and the group's pipelines link the nanostructure of organic solar cells to their performance.

**Materials by computation.** Graph-based methods and fast virtual instruments turn hard-to-read microscopy and X-ray data into actionable design information, letting experimentalists ask sharper questions and get quantitative answers.

**Simulation at scale.** New high-performance methods solve complex-geometry flow, heat transfer, and time-dependent problems on leadership-class supercomputers, from soft-matter manufacturing to the airflow inside buildings.

**Training the AI workforce.** More than fifty PhD and MS graduates have gone on to national laboratories (NASA, Argonne, ORNL, PNNL), to industry (Bayer, John Deere, Corning, Micron, Intel), and to faculty positions worldwide. See the [alumni wall](/people/).

<div class="impact-cta">
  <h3>Let's build what comes next</h3>
  <p>We have bold new plans taking shape. If you are a <strong>policy maker</strong> or a <strong>philanthropic partner</strong>, we would welcome a conversation, whether about the work described here or where we intend to take it next. Please <a href="mailto:{{ 'baskarg@iastate.edu' | encode_email }}?subject=Connecting%20with%20the%20Baskar%20Group">email Baskar Ganapathysubramanian</a> to start the discussion.</p>
</div>

<p class="impact-todo">TODO(baskar): specific reach numbers (growers, acres, people reached) and two or three full impact stories with a hero image each.</p>

<style>
  .stats-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0 2rem; }
  .stat { border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 10px; padding: 1rem; text-align: center; }
  .stat-value { font-size: 1.9rem; font-weight: 800; color: var(--global-theme-color, #b31b1b); line-height: 1.1; }
  .stat-label { font-size: .82rem; margin-top: .3rem; }
  .stat-note { font-size: .72rem; color: var(--global-text-color-light, #828282); margin-top: .2rem; }
  .impact-cta { border: 1px solid var(--global-divider-color, #e0e0e0); border-left: 4px solid var(--global-theme-color, #b31b1b); border-radius: 8px; padding: 1.1rem 1.3rem; margin: 2rem 0 1rem; background: rgba(179, 27, 27, .04); }
  .impact-cta h3 { margin: 0 0 .4rem; font-size: 1.2rem; }
  .impact-cta p { margin: 0; }
  .impact-todo { margin-top: 1.5rem; font-size: .85rem; color: var(--global-text-color-light, #828282); }
</style>
