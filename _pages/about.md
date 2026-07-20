---
layout: about
title: about
permalink: /
subtitle: Computational sustainability at Iowa State University.

profile:
  align: right
  image: people/baskar.webp
  image_circular: false # crops the image to make it circular
  more_info: >
    <p><strong>Baskar Ganapathysubramanian</strong>, Distinguished Professor of Engineering, Iowa State University.</p>
    <p>Director, <a href="https://aiira.iastate.edu/">AI Institute for Resilient Agriculture</a>. Associate Director, <a href="https://trac-ai.iastate.edu/">Translational AI Center</a>.</p>
    <p><a href="https://www.engineering.iastate.edu/people/profile/baskarg/">Iowa State profile and contact</a>.</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # re-enable once _news has items (seed via /add-win)
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
---

<img class="home-hero" src="{{ '/assets/img/hero-streamlines.webp' | relative_url }}" alt="Simulation streamlines from a Baskar Group flow computation">

We build computational tools that help solve national challenges in food, energy, environment, and health: identifying crop pests from a phone photo, simulating how air and heat move through buildings and cities, and designing the materials inside next generation electronics. Baskar Ganapathysubramanian directs the [AI Institute for Resilient Agriculture (AIIRA)](https://aiira.iastate.edu/), a 20 million dollar national AI institute, and is Associate Director of the [Translational AI Center (TrAC)](https://trac-ai.iastate.edu/).

We are a computational sustainability group. We combine applied mathematics, scientific computing, and machine learning to model, design, and control complex physical systems. Recent work spans flow physics across complex geometries such as buildings and vehicles, charge transport in organic electronics and electrochemical systems, soft matter manufacturing, and resilient agriculture. We develop the mathematical techniques and computational tools, including model reduction, multiscale frameworks, multiphysics simulators, control algorithms, and data-driven methods, that make these problems tractable.

Our group is very collaborative and is always looking for enthusiastic students, postdocs, and collaborators. See [Join](/join/) if you want to work at the intersection of simulation science, data science, and sustainability.

<h2 class="home-themes-head">Research themes</h2>
<div class="home-themes">
{% for theme in site.data.themes %}
  {% assign cnt = site.data.theme_counts[theme.slug] %}
  <a class="home-theme" href="{{ '/research/#' | append: theme.slug | relative_url }}">
    <span class="home-theme-name">{{ theme.name }}{% if cnt %}<span class="home-theme-count">{{ cnt }}</span>{% endif %}</span>
    <span class="home-theme-blurb">{{ theme.blurb }}</span>
  </a>
{% endfor %}
</div>

<style>
  .home-hero { clear: both; width: 100%; height: auto; border-radius: 10px; margin: .5rem 0 1.3rem; display: block; }
  .home-centers { margin-top: 1.2rem; font-size: .95rem; }
  .home-themes-head { margin-top: 2rem; }
  .home-themes { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: .8rem; margin: 1rem 0 .5rem; }
  .home-theme { display: block; border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 10px; padding: .7rem .9rem; text-decoration: none; color: inherit; transition: border-color .15s; }
  .home-theme:hover { border-color: var(--global-theme-color, #b31b1b); }
  .home-theme-name { font-weight: 700; display: flex; justify-content: space-between; align-items: center; gap: .5rem; }
  .home-theme-count { background: var(--global-theme-color, #b31b1b); color: #fff; border-radius: 999px; padding: 0 .5rem; font-size: .72rem; font-weight: 600; }
  .home-theme-blurb { display: block; font-size: .8rem; color: var(--global-text-color-light, #828282); margin-top: .35rem; line-height: 1.35; }
</style>
