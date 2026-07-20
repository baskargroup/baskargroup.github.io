---
layout: page
title: People
permalink: /people/
nav: true
nav_order: 4
description: Members of the Baskar Group.
---

{% assign cur_roles = "pi,staff,postdoc,phd,ms" | split: "," %}
{% assign cur_labels = "Principal Investigator|Research Staff|Postdoctoral Researchers|PhD Students|MS Students" | split: "|" %}

{% for role in cur_roles %}
  {% assign members = site.people | where: "role", role | sort: "start_sort" %}
  {% if members.size > 0 %}
<h2 class="people-role">{{ cur_labels[forloop.index0] }}</h2>
<div class="people-grid">
{% for p in members %}
  {% assign photo = p.photo | default: "/assets/img/prof_pic.jpg" %}
  {% assign pq = p.name | url_encode %}
  <div class="person-card">
    <img class="person-photo" src="{{ photo | relative_url }}" alt="{{ p.name }}" loading="lazy">
    <div class="person-name"><a href="{{ '/publications/' | relative_url }}?q={{ pq }}">{{ p.name }}</a></div>
    <div class="person-meta">
      {% if p.title %}{{ p.title }}{% elsif p.started != "" %}Since {{ p.started }}{% endif %}
      {% if p.coadvisors != "" %}<br>co-advised with {{ p.coadvisors }}{% endif %}
    </div>
  </div>
{% endfor %}
</div>
  {% endif %}
{% endfor %}

<h2 class="people-role">Alumni</h2>
{% assign al_types = "phd,ms,postdoc" | split: "," %}
{% assign al_labels = "PhD|MS|Former Postdocs" | split: "|" %}
{% for t in al_types %}
  {% assign alums = site.people | where: "role", "alumni" | where: "alumni_type", t | sort: "grad_year" | reverse %}
  {% if alums.size > 0 %}
<h3 class="alumni-group">{{ al_labels[forloop.index0] }} ({{ alums.size }})</h3>
<ul class="alumni-list">
{% for p in alums %}
  {% assign pq = p.name | url_encode %}
  <li>
    <span class="alumni-when">{% if p.alumni_type == "postdoc" and p.years %}{{ p.years }}{% else %}{{ p.grad_year }}{% endif %}</span>
    <a href="{{ '/publications/' | relative_url }}?q={{ pq }}">{{ p.name }}</a>{% if p.coadvisors != "" %} <span class="alumni-co">(co-advised with {{ p.coadvisors }})</span>{% endif %}{% if p.placement != "" %} &rarr; <span class="alumni-place">{{ p.placement }}</span>{% endif %}
  </li>
{% endfor %}
</ul>
  {% endif %}
{% endfor %}

<p class="people-note">TODO(baskar): member photos and personal links. Alumni placements are from the July 2026 CV; update any that have changed.</p>

<style>
  .people-role { margin-top: 2.2rem; }
  .people-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1.25rem; margin-bottom: 1rem; }
  .person-card { text-align: center; }
  .person-photo { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; background: #ececec; }
  .person-name { font-weight: 600; margin-top: .4rem; font-size: .95rem; line-height: 1.2; }
  .person-meta { font-size: .78rem; color: var(--global-text-color-light, #828282); margin-top: .2rem; }
  .alumni-group { margin-top: 1.4rem; font-size: 1.05rem; }
  .alumni-list { list-style: none; padding-left: 0; }
  .alumni-list li { padding: .3rem 0; border-bottom: 1px solid var(--global-divider-color, #eee); font-size: .92rem; }
  .alumni-when { display: inline-block; min-width: 4.5rem; color: var(--global-text-color-light, #828282); font-variant-numeric: tabular-nums; }
  .alumni-co { color: var(--global-text-color-light, #828282); font-size: .85em; }
  .alumni-place { color: var(--global-theme-color, #b31b1b); }
  .people-note { margin-top: 2rem; font-size: .85rem; color: var(--global-text-color-light, #828282); }
</style>
