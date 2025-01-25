---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

{% include section.html %}

## PI

{% include list-name.html data="members" component="portrait" filter="role == 'pi'" %}

## Researchers

{% include list-name.html data="members" component="portrait" filter="role == 'researcher'" %}

## PhD Students

{% include list-name.html data="members" component="portrait" filter="role == 'phd'" %}

## Alumni

{% include list.html data="members" component="portrait" filter="role == 'alumni'" %}<br>
