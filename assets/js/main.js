document.addEventListener('DOMContentLoaded', function() {
  initToggleSwitches();
  initContactForm();
  initCardEffects();
  initImageErrorHandling();
  initStatsCounter();
  initMobileMenu();
  initScrollEffects();
  initProjectFilter();
  initFaq();
  initTestimonialsSlider();
  initServiceCards();
  initProjectsFilter();
  initTestimonialsNav();
  initSmoothScroll();
  initPanorama();
});

function initMobileMenu() {
  const hamburger = document.querySelector('.hamburger-menu');
  const nav = document.querySelector('.nav');
  const navLinks = document.querySelectorAll('.nav-item a');
  
  if (hamburger && nav) {
    hamburger.addEventListener('click', function() {
      hamburger.classList.toggle('active');
      nav.classList.toggle('active');
    });
    
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        hamburger.classList.remove('active');
        nav.classList.remove('active');
      });
    });
  }
}

function initScrollEffects() {
  const header = document.querySelector('.header');
  const floatCta = document.getElementById('floatCta');
  let lastScrollY = window.scrollY;
  
  if (!header) return;
  
  window.addEventListener('scroll', function() {
    const currentScrollY = window.scrollY;
    
    if (currentScrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    if (floatCta) {
      if (currentScrollY > 300) {
        floatCta.style.opacity = '1';
        floatCta.style.transform = 'translateY(0)';
      } else {
        floatCta.style.opacity = '0';
        floatCta.style.transform = 'translateY(20px)';
      }
    }
    
    lastScrollY = currentScrollY;
  }, { passive: true });
}

function initStatsCounter() {
  const counters = document.querySelectorAll('.stat-number, .hero-stat-num');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counter = entry.target;
        const target = parseInt(counter.dataset.count || counter.dataset.target);
        if (!isNaN(target)) {
          animateCounter(counter, target);
        }
        observer.unobserve(counter);
      }
    });
  }, { threshold: 0.5 });
  
  counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target) {
  let current = 0;
  const duration = 2000;
  const increment = target / (duration / 16);
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    element.textContent = Math.floor(current);
  }, 16);
}

function initImageErrorHandling() {
  const images = document.querySelectorAll('img');
  
  images.forEach(img => {
    img.addEventListener('error', function() {
      const cardImage = this.closest('.card-image');
      const productImage = this.closest('.product-card');
      
      if (cardImage) {
        cardImage.style.background = 'linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(123, 47, 247, 0.1))';
        cardImage.style.display = 'flex';
        cardImage.style.alignItems = 'center';
        cardImage.style.justifyContent = 'center';
        this.style.display = 'none';
        
        const icon = document.createElement('div');
        icon.className = 'image-placeholder';
        icon.textContent = this.alt ? this.alt.charAt(0) : '🖼️';
        cardImage.appendChild(icon);
      } else if (productImage) {
        this.style.display = 'none';
        const placeholder = document.createElement('div');
        placeholder.className = 'product-placeholder';
        placeholder.textContent = this.alt ? this.alt.charAt(0) : '🏠';
        productImage.insertBefore(placeholder, productImage.firstChild);
      } else {
        this.src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMjAwIDE1MCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIxNTAiIGZpbGw9IiMzMzMiLz48cGF0aCBkPSJNMTgwIDEwMEwxNjAgMTMwSDQwTDIwIDEwMHYyNGgxNjB2LTI0eiIvPjwvc3ZnPg==';
        this.alt = '图片加载失败';
      }
    });
    
    img.addEventListener('load', function() {
      this.style.opacity = '1';
    });
  });
}

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

function initProjectFilter() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card-new');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const filter = this.dataset.filter;
      
      projectCards.forEach(card => {
        if (filter === 'all') {
          card.style.display = 'block';
        } else {
          if (card.dataset.category === filter) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        }
      });
    });
  });
}

function initFaq() {
  const faqQuestions = document.querySelectorAll('.faq-question');
  const categoryBtns = document.querySelectorAll('.category-btn');
  const faqSections = document.querySelectorAll('.faq-section');

  faqQuestions.forEach(question => {
    question.addEventListener('click', function() {
      const faqItem = this.parentElement;
      const isActive = faqItem.classList.contains('active');
      
      document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
      });
      
      if (!isActive) {
        faqItem.classList.add('active');
      }
    });
  });

  categoryBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      categoryBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const category = this.dataset.category;
      
      faqSections.forEach(section => {
        if (category === 'all') {
          section.classList.remove('hidden');
        } else {
          if (section.dataset.category === category) {
            section.classList.remove('hidden');
          } else {
            section.classList.add('hidden');
          }
        }
      });
    });
  });
}

function initTestimonialsSlider() {
  const slider = document.getElementById('testimonialsSlider');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const navDots = document.getElementById('navDots');
  const cards = document.querySelectorAll('.testimonial-card');
  
  if (!slider || !cards.length) return;
  
  const cardsPerPage = 3;
  const totalPages = Math.ceil(cards.length / cardsPerPage);
  let currentPage = 0;
  
  for (let i = 0; i < totalPages; i++) {
    const dot = document.createElement('div');
    dot.className = 'nav-dot';
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToPage(i));
    navDots.appendChild(dot);
  }
  
  const dots = document.querySelectorAll('.nav-dot');
  
  function updateSlider() {
    const offset = -currentPage * 100;
    slider.style.transform = `translateX(${offset}%)`;
    
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentPage);
    });
    
    prevBtn.disabled = currentPage === 0;
    nextBtn.disabled = currentPage === totalPages - 1;
  }
  
  function goToPage(page) {
    if (page >= 0 && page < totalPages) {
      currentPage = page;
      updateSlider();
    }
  }
  
  prevBtn.addEventListener('click', () => goToPage(currentPage - 1));
  nextBtn.addEventListener('click', () => goToPage(currentPage + 1));
  
  updateSlider();
}

function initServiceCards() {
  const cards = document.querySelectorAll('.service-card-new');
  
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.classList.add('hovered');
    });
    
    card.addEventListener('mouseleave', function() {
      this.classList.remove('hovered');
    });
  });
}

function initProjectsFilter() {
  const filterBtns = document.querySelectorAll('.projects-filters .filter-btn');
  const projectCards = document.querySelectorAll('.project-card-new');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const filter = this.dataset.filter;
      
      projectCards.forEach(card => {
        if (filter === 'all') {
          card.style.display = 'block';
        } else {
          if (card.dataset.category === filter) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        }
      });
    });
  });
}

function initTestimonialsNav() {
  const navBtns = document.querySelectorAll('.testimonials-nav button');
  const cards = document.querySelectorAll('.testimonial-card-new');
  
  navBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      navBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const direction = this.dataset.direction;
      const container = document.querySelector('.testimonials-grid');
      
      if (!container) return;
      
      const scrollAmount = direction === 'prev' ? -320 : 320;
      container.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    });
  });
}

function initSmoothScroll() {
  const links = document.querySelectorAll('a[href*="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      const hashIndex = href.indexOf('#');
      if (hashIndex === -1) return;
      
      const hash = href.substring(hashIndex);
      const pagePath = href.substring(0, hashIndex);
      
      const currentPage = window.location.pathname.split('/').pop();
      const targetPage = pagePath || 'index.html';
      
      if (currentPage !== targetPage) return;
      
      const target = document.querySelector(hash);
      if (target) {
        e.preventDefault();
        const offsetTop = target.offsetTop - 80;
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    });
  });
}

function initPanorama() {
  const panorama = document.getElementById('panorama');
  if (!panorama) return;
  
  let isDragging = false;
  let startX = 0;
  let currentPos = 50;
  
  panorama.addEventListener('mousedown', function(e) {
    isDragging = true;
    startX = e.clientX;
    panorama.style.transition = 'none';
  });
  
  panorama.addEventListener('mousemove', function(e) {
    if (!isDragging) return;
    
    const deltaX = e.clientX - startX;
    const deltaPercent = deltaX / window.innerWidth * 100;
    
    currentPos -= deltaPercent;
    currentPos = Math.max(0, Math.min(100, currentPos));
    
    panorama.style.backgroundPosition = `${currentPos}% center`;
    startX = e.clientX;
  });
  
  panorama.addEventListener('mouseup', function() {
    isDragging = false;
    panorama.style.transition = 'background-position 0.1s ease-out';
  });
  
  panorama.addEventListener('mouseleave', function() {
    isDragging = false;
    panorama.style.transition = 'background-position 0.1s ease-out';
  });
  
  panorama.addEventListener('touchstart', function(e) {
    isDragging = true;
    startX = e.touches[0].clientX;
    panorama.style.transition = 'none';
  });
  
  panorama.addEventListener('touchmove', function(e) {
    if (!isDragging) return;
    
    const deltaX = e.touches[0].clientX - startX;
    const deltaPercent = deltaX / window.innerWidth * 100;
    
    currentPos -= deltaPercent;
    currentPos = Math.max(0, Math.min(100, currentPos));
    
    panorama.style.backgroundPosition = `${currentPos}% center`;
    startX = e.touches[0].clientX;
  });
  
  panorama.addEventListener('touchend', function() {
    isDragging = false;
    panorama.style.transition = 'background-position 0.1s ease-out';
  });
}