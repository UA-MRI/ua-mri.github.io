---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

{% include section.html %}

{% include list-name.html data="members" component="portrait" filter="role == 'pi'" %}
{% include list-name.html data="members" component="portrait" filter="role != 'pi'" %}
