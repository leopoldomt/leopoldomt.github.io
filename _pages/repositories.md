---
layout: page
permalink: /repositories/
title: repositories
nav: false
---

{% for repo in site.data.repositories.github_repos %}
- [{{ repo }}](https://github.com/{{ repo }})
{% endfor %}

[My GitHub profile](https://github.com/leopoldomt)
