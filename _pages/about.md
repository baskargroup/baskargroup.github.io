---
layout: about
title: about
permalink: /
subtitle: Computational sustainability at Iowa State University.

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # re-enable once _news has items (seed via /add-win)
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
---

<div class="home-hero-wrap">
  <video class="home-hero" autoplay muted loop playsinline poster="{{ '/assets/img/hero-proteus.webp' | relative_url }}" aria-label="Two-phase jet simulation from the group's Proteus solver">
    <source src="{{ '/assets/video/phi_jet.mp4' | relative_url }}" type="video/mp4">
  </video>
  <div class="home-hero-caption">Computational tools for food, energy, environment, and health</div>
</div>
<script>
  // Respect reduced-motion: pause the hero loop, leaving the poster frame.
  (function () { var v = document.querySelector('.home-hero');
    if (v && window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) { v.removeAttribute('autoplay'); if (v.pause) v.pause(); } })();
</script>

We build computational tools that help solve societal challenges in food, energy, environment, and health: identifying crop pests from a phone photo, simulating how air and heat move through buildings, and designing the materials inside next generation electronics. Baskar Ganapathysubramanian directs the [AI Institute for Resilient Agriculture (AIIRA)](https://aiira.iastate.edu/), a 20 million dollar national AI institute, and is Associate Director of the [Translational AI Center (TrAC)](https://trac-ai.iastate.edu/).

We are always looking for curious students, postdocs, and collaborators. See [Join](/join/) to work with us.

<h2 class="home-themes-head">Research themes</h2>
<div class="home-themes">
{% for theme in site.data.themes %}
  {% assign cnt = site.data.theme_counts[theme.slug] %}
  <a class="home-theme" href="{{ '/research/#' | append: theme.slug | relative_url }}">
    <span class="home-theme-name">{{ theme.name }}</span>
    {% if cnt %}<span class="home-theme-count">{{ cnt }}</span>{% endif %}
  </a>
{% endfor %}
</div>

<style>
  .home-hero-wrap { position: relative; clear: both; margin: .5rem 0 1.4rem; }
  .home-hero { display: block; width: 100%; max-height: 44vh; object-fit: cover; border-radius: 10px; }
  .home-hero-caption { position: absolute; left: 0; right: 0; bottom: 0; padding: 1.4rem 1.2rem .9rem; color: #fff; font-size: 1.15rem; font-weight: 600; line-height: 1.25; background: linear-gradient(to top, rgba(0,0,0,.72), rgba(0,0,0,0)); border-radius: 0 0 10px 10px; }
  .home-themes-head { margin-top: 2rem; }
  .home-themes { display: grid; grid-template-columns: repeat(auto-fill, minmax(185px, 1fr)); gap: .55rem; margin: 1rem 0 .5rem; }
  .home-theme { display: flex; justify-content: space-between; align-items: center; gap: .5rem; border: 1px solid var(--global-divider-color, #e0e0e0); border-radius: 8px; padding: .5rem .75rem; text-decoration: none; color: inherit; transition: border-color .15s; }
  .home-theme:hover { border-color: var(--global-theme-color, #b31b1b); }
  .home-theme-name { font-weight: 600; font-size: .9rem; }
  .home-theme-count { background: var(--global-theme-color, #b31b1b); color: #fff; border-radius: 999px; padding: 0 .5rem; font-size: .72rem; font-weight: 600; }
  @media (max-width: 576px) {
    .home-hero { max-height: 38vh; }
    .home-hero-caption { font-size: 1rem; padding: 1rem .9rem .7rem; }
    .home-theme { min-height: 40px; }
  }
</style>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Baskar Group",
  "alternateName": "Ganapathysubramanian Group",
  "url": "https://baskar-group.github.io/",
  "description": "Computational tools for societal challenges in food, energy, environment, and health, at Iowa State University.",
  "parentOrganization": { "@type": "CollegeOrUniversity", "name": "Iowa State University", "url": "https://www.iastate.edu/" },
  "founder": {
    "@type": "Person",
    "name": "Baskar Ganapathysubramanian",
    "jobTitle": "Distinguished Professor of Engineering",
    "affiliation": { "@type": "CollegeOrUniversity", "name": "Iowa State University" },
    "memberOf": [
      { "@type": "Organization", "name": "AI Institute for Resilient Agriculture (AIIRA)", "url": "https://aiira.iastate.edu/" },
      { "@type": "Organization", "name": "Translational AI Center (TrAC)", "url": "https://trac-ai.iastate.edu/" }
    ],
    "sameAs": [
      "https://www.engineering.iastate.edu/people/profile/baskarg/",
      "https://scholar.google.com/citations?user=R1JIs4cAAAAJ",
      "https://orcid.org/0000-0002-8931-4852"
    ]
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "inquiries",
    "url": "https://www.engineering.iastate.edu/people/profile/baskarg/"
  }
}
</script>
