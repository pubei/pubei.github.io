document.addEventListener('DOMContentLoaded', function() {
  initToggleSwitches();
  initContactForm();
  initCardEffects();
});

function initToggleSwitches() {
  const toggles = document.querySelectorAll('.toggle-switch');
  
  toggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      this.classList.toggle('active');
    });
  });
}

function initContactForm() {
  const form = document.getElementById('contactForm');
  
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData(this);
      const data = Object.fromEntries(formData);
      
      alert(`感谢您的预约！\n\n姓名：${data.name}\n电话：${data.phone}\n服务类型：${data.service}\n房屋面积：${data.area || '未填写'}\n留言：${data.message || '无'}\n\n我们会尽快与您联系！`);
      
      this.reset();
    });
  }
}

function initCardEffects() {
  const cards = document.querySelectorAll('.card, .service-card, .project-card');
  
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px) scale(1.01)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });
}
