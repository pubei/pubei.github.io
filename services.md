---
layout: default
title: 服务项目 - 浦北装修设计公司
---

<h1 class="page-title">服务项目</h1>

<div class="container">
  <div class="services-grid">
    {% for service in site.data.services %}
      <div class="service-card">
        <h3>{{ service.icon }} {{ service.name }}</h3>
        <p>{{ service.description }}</p>
        <ul>
          {% for feature in service.features %}
            <li>{{ feature }}</li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </div>
</div>
