---
layout: page
title: People
permalink: /people/
nav: true
nav_order: 4
description: Members of the Baskar Group.
---

{% assign cur_roles = "pi,staff,postdoc,phd,ms" | split: "," %}
{% assign cur_labels = "Principal Investigator|Staff|Postdoctoral Researchers|PhD Students|MS Students" | split: "|" %}

{% capture ic_linkedin %}<svg class="picon" viewBox="0 0 448 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 53.79 0 0 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.29 0-55.69 37.7-55.69 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.69-48.3 87.88-48.3 94 0 111.28 61.9 111.28 142.3V448z"/></svg>{% endcapture %}
{% capture ic_scholar %}<svg class="picon" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><circle cx="256" cy="362" r="150" fill="currentColor"/><path fill="currentColor" d="M256 411.12L0 202.667 256 0l256 202.667z"/></svg>{% endcapture %}
{% capture ic_site %}<svg class="picon" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M352 256c0 22.2-1.2 43.6-3.3 64H163.3c-2.2-20.4-3.3-41.8-3.3-64s1.2-43.6 3.3-64H348.7c2.2 20.4 3.3 41.8 3.3 64zm28.8-64H503.9c5.3 20.5 8.1 41.9 8.1 64s-2.8 43.5-8.1 64H380.8c2.1-20.6 3.2-42 3.2-64s-1.1-43.4-3.2-64zm112.6-32H376.7c-10-63.9-29.8-117.4-55.3-151.6c78.3 20.7 142 77.5 171.9 151.6zm-149.1 0H167.7c6.1-36.4 15.5-68.6 27-94.7c10.5-23.6 22.2-40.7 33.5-51.5C239.4 3.2 248.7 0 256 0s16.6 3.2 27.8 13.8c11.3 10.8 23 27.9 33.5 51.5c11.6 26 20.9 58.2 27 94.7zm-209 0H18.6C48.6 85.9 112.2 29.1 190.6 8.4C165.1 42.6 145.3 96.1 135.3 160zM8.1 192H131.2c-2.1 20.6-3.2 42-3.2 64s1.1 43.4 3.2 64H8.1C2.8 299.5 0 278.1 0 256s2.8-43.5 8.1-64zM194.7 446.6c-11.6-26-20.9-58.2-27-94.6H344.3c-6.1 36.4-15.5 68.6-27 94.6c-10.5 23.6-22.2 40.7-33.5 51.5C272.6 508.8 263.3 512 256 512s-16.6-3.2-27.8-13.8c-11.3-10.8-23-27.9-33.5-51.5zM135.3 352c10 63.9 29.8 117.4 55.3 151.6C112.2 482.9 48.6 426.1 18.6 352H135.3zm358.1 0c-30 74.1-93.6 130.9-171.9 151.6c25.5-34.2 45.3-87.7 55.3-151.6H493.4z"/></svg>{% endcapture %}

{% for role in cur_roles %}
  {% assign members = site.people | where: "role", role | sort: "start_sort" %}
  {% if members.size > 0 %}
<h2 class="people-role">{{ cur_labels[forloop.index0] }}</h2>
<div class="people-grid">
{% for p in members %}
  {% assign photo = p.photo | default: "/assets/img/people/silhouette.svg" %}
  {% assign pq = p.name | url_encode %}
  <div class="person-card">
    <img class="person-photo" src="{{ photo | relative_url }}" alt="{{ p.name }}" loading="lazy">
    <div class="person-name"><a href="{{ '/publications/' | relative_url }}?member={{ p.slug }}&mname={{ pq }}">{{ p.name }}</a></div>
    <div class="person-meta">
      {% if p.role == "pi" or p.role == "staff" %}{{ p.title }}{% elsif p.started != "" %}Since {{ p.started }}{% endif %}
      {% if p.affiliation %}<br>{{ p.affiliation }}{% endif %}
      {% if p.coadvisors != "" %}<br>co-advised with {{ p.coadvisors }}{% endif %}
    </div>
    {% if p.social.linkedin or p.links.scholar or p.links.site %}
    <div class="person-links">
      {% if p.social.linkedin %}<a class="plink" href="{{ p.social.linkedin }}" target="_blank" rel="noopener" aria-label="{{ p.name }} on LinkedIn">{{ ic_linkedin }}</a>{% endif %}
      {% if p.links.scholar %}<a class="plink" href="{{ p.links.scholar }}" target="_blank" rel="noopener" aria-label="{{ p.name }} on Google Scholar">{{ ic_scholar }}</a>{% endif %}
      {% if p.links.site %}<a class="plink" href="{{ p.links.site }}" target="_blank" rel="noopener" aria-label="{{ p.name }} personal website">{{ ic_site }}</a>{% endif %}
    </div>
    {% endif %}
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
    <a href="{{ '/publications/' | relative_url }}?member={{ p.slug }}&mname={{ pq }}">{{ p.name }}</a>{% if p.coadvisors != "" %} <span class="alumni-co">(co-advised with {{ p.coadvisors }})</span>{% endif %}{% if p.placement != "" %} &rarr; <span class="alumni-place">{{ p.placement }}</span>{% endif %}
  </li>
{% endfor %}
</ul>
  {% endif %}
{% endfor %}

<p class="people-note">TODO(baskar): a few current members still need a photo or personal links. Alumni placements are from the July 2026 CV; update any that have changed.</p>

<style>
  .people-role { margin-top: 2.2rem; }
  .people-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1.25rem; margin-bottom: 1rem; }
  .person-card { text-align: center; }
  .person-photo { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; background: #ececec; }
  .person-name { font-weight: 600; margin-top: .4rem; font-size: .95rem; line-height: 1.2; }
  .person-meta { font-size: .78rem; color: var(--global-text-color-light, #828282); margin-top: .2rem; }
  .person-links { margin-top: .4rem; display: flex; justify-content: center; gap: .55rem; }
  .person-links .plink { display: inline-flex; line-height: 0; color: var(--global-text-color-light, #828282); transition: color .15s ease; }
  .person-links .plink:hover { color: var(--global-theme-color, #0e7490); }
  .picon { width: 16px; height: 16px; display: block; }
  .alumni-group { margin-top: 1.4rem; font-size: 1.05rem; }
  .alumni-list { list-style: none; padding-left: 0; }
  .alumni-list li { padding: .3rem 0; border-bottom: 1px solid var(--global-divider-color, #eee); font-size: .92rem; }
  .alumni-when { display: inline-block; min-width: 4.5rem; color: var(--global-text-color-light, #828282); font-variant-numeric: tabular-nums; }
  .alumni-co { color: var(--global-text-color-light, #828282); font-size: .85em; }
  .alumni-place { color: var(--global-theme-color, #0e7490); }
  .people-note { margin-top: 2rem; font-size: .85rem; color: var(--global-text-color-light, #828282); }
</style>
