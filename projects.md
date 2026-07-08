---
layout: default
title: 装修案例 - 浦北装修设计公司
---

<h1 class="page-title">装修案例</h1>

<div class="container">
  <div class="projects-grid">
    {% for project in site.data.projects %}
      <div class="project-card">
        <div class="gallery-item">{{ project.images }}</div>
        <h3>{{ project.name }}</h3>
        <p><strong>类别：</strong>{{ project.category }}</p>
        <p><strong>面积：</strong>{{ project.area }}</p>
        <p><strong>预算：</strong>{{ project.budget }}</p>
        <p><strong>状态：</strong>{{ project.status }}</p>
        <p>{{ project.description }}</p>
      </div>
    {% endfor %}
  </div>
</div>
