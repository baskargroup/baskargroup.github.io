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
    <p>TODO(baskar): office and contact.</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
---

The Baskar Group is a computational sustainability group at Iowa State University. We leverage applied mathematics, scientific computation, and machine learning to model, design, and control complex systems, with application to food, energy and environment, and health.

We are particularly interested in energy and environment related phenomena. Recent examples include flow physics across complex geometries such as buildings and vehicles, charge transport in organic electronic devices and electrochemical systems, coupled phenomena during soft matter manufacturing, and enabling resilient agriculture. We develop mathematical techniques and computational tools (model reduction, multiscale frameworks, multiphysics simulators, control algorithms, and data-driven methods) to efficiently represent these systems.

Our group is very collaborative and is always looking for enthusiastic students, postdocs, and collaborators. If you are interested in working at the intersection of simulation science, data science, and sustainability applications, please reach out.

<p class="home-centers">Baskar directs the <a href="https://aiira.iastate.edu/">AI Institute for Resilient Agriculture (AIIRA)</a> and is Associate Director of the <a href="https://trac-ai.iastate.edu/">Translational AI Center (TrAC)</a> at Iowa State University.</p>

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
  .home-centers { margin-top: 1.2rem; font-size: .95rem; }
  .home-themes-head { margin-top: 2rem; }
  .home-themes { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: .8rem; margin: 1rem 0 .5rem; }
  .home-theme { display: block; border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 10px; padding: .7rem .9rem; text-decoration: none; color: inherit; transition: border-color .15s; }
  .home-theme:hover { border-color: var(--global-theme-color, #b31b1b); }
  .home-theme-name { font-weight: 700; display: flex; justify-content: space-between; align-items: center; gap: .5rem; }
  .home-theme-count { background: var(--global-theme-color, #b31b1b); color: #fff; border-radius: 999px; padding: 0 .5rem; font-size: .72rem; font-weight: 600; }
  .home-theme-blurb { display: block; font-size: .8rem; color: var(--global-text-color-light, #828282); margin-top: .35rem; line-height: 1.35; }
</style>
