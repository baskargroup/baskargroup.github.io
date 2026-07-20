---
layout: page
title: People
permalink: /people/
nav: true
nav_order: 4
description: Members of the Baskar Group.
---

{% assign roles = "pi,postdoc,phd,ms,staff" | split: "," %}
{% assign labels = "Principal Investigator|Postdoctoral Researchers|PhD Students|MS Students|Staff" | split: "|" %}

{% for role in roles %}
  {% assign members = site.people | where: "role", role | sort: "start_sort" %}
  {% if members.size > 0 %}
<h2 class="people-role">{{ labels[forloop.index0] }}</h2>
<div class="people-grid">
{% for p in members %}
  {% assign photo = p.photo | default: "/assets/img/prof_pic.jpg" %}
  {% assign pq = p.name | url_encode %}
  <div class="person-card">
    <img class="person-photo" src="{{ photo | relative_url }}" alt="{{ p.name }}" loading="lazy">
    <div class="person-name"><a href="{{ '/publications/' | relative_url }}?q={{ pq }}">{{ p.name }}</a></div>
    <div class="person-meta">
      {% if p.started != "" %}Since {{ p.started }}{% endif %}
      {% if p.coadvisors != "" %}<br>co-advised with {{ p.coadvisors }}{% endif %}
    </div>
  </div>
{% endfor %}
</div>
  {% endif %}
{% endfor %}

<p class="people-note">Alumni (29 PhD and 16 MS graduates, plus postdoctoral alumni) will be added as a grouped alumni wall from the CV records. TODO(baskar): member photos and links.</p>

<style>
  .people-role { margin-top: 2rem; }
  .people-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1.25rem; margin-bottom: 1rem; }
  .person-card { text-align: center; }
  .person-photo { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; background: #ececec; }
  .person-name { font-weight: 600; margin-top: .4rem; font-size: .95rem; line-height: 1.2; }
  .person-meta { font-size: .78rem; color: var(--global-text-color-light, #828282); margin-top: .2rem; }
  .people-note { margin-top: 2rem; font-size: .85rem; color: var(--global-text-color-light, #828282); }
</style>
