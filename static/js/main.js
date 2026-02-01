document.addEventListener('DOMContentLoaded', function() {
    const header = document.getElementById('header');
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
            
            const spans = menuToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
                const spans = menuToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }

    const statsTabs = document.querySelectorAll('.stats-tab');
    const brStats = document.getElementById('br-stats');
    const mpStats = document.getElementById('mp-stats');

    if (statsTabs.length > 0 && brStats && mpStats) {
        statsTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                statsTabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');

                const tabType = this.getAttribute('data-tab');
                if (tabType === 'br') {
                    brStats.style.display = 'block';
                    mpStats.style.display = 'none';
                } else if (tabType === 'mp') {
                    brStats.style.display = 'none';
                    mpStats.style.display = 'block';
                }
            });
        });
    }

    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            window.location.href = 'profile.html';
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (password !== confirmPassword) {
                alert('Les mots de passe ne correspondent pas.');
                return;
            }
            
            window.location.href = 'profile.html';
        });
    }

    const socialBtns = document.querySelectorAll('.btn-social');
    socialBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const provider = this.classList.contains('btn-google') ? 'Google' : 'Discord';
            alert(`Connexion avec ${provider} - Fonctionnalité simulée`);
        });
    });

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animateElements = document.querySelectorAll('.feature-card, .stat-card, .tournament-card, .blog-card');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    const navLinks = document.querySelectorAll('.nav-link');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    const statValues = document.querySelectorAll('.stat-value, .hero-stat-value');
    
    function animateValue(element, start, end, duration) {
        const range = end - start;
        const startTime = performance.now();
        
        function updateValue(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = start + (range * easeOutQuart);
            
            if (element.dataset.suffix) {
                element.textContent = Math.floor(current).toLocaleString() + element.dataset.suffix;
            } else if (element.dataset.decimal) {
                element.textContent = current.toFixed(2);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            }
        }
        
        requestAnimationFrame(updateValue);
    }

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function(e) {
            const x = e.clientX - this.getBoundingClientRect().left;
            const y = e.clientY - this.getBoundingClientRect().top;
            
            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                width: 0;
                height: 0;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                left: ${x}px;
                top: ${y}px;
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });

    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                width: 200px;
                height: 200px;
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});
