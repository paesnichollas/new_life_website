// New Life - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling para links âncora
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Compensar navbar fixa
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Navbar background change on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Animação de entrada para elementos
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animateElements = document.querySelectorAll('.category-card, .product-card, .testimonial-card, .contact-item');
    animateElements.forEach(el => {
        observer.observe(el);
    });
    
    // Lazy loading para imagens
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
    
    // Validação de formulário aprimorada
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Remover classe de erro quando o usuário começar a digitar
                    field.addEventListener('input', function() {
                        this.classList.remove('is-invalid');
                    });
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Scroll para o primeiro campo com erro
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            }
        });
    });
    
    // Tooltip initialization (se Bootstrap tooltips estiverem sendo usados)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Efeito parallax suave para o hero banner
    const heroSection = document.querySelector('.hero-banner');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            const heroBackground = heroSection.querySelector('.hero-bg');
            if (heroBackground) {
                heroBackground.style.transform = `translateY(${rate}px)`;
            }
        });
    }
    
    // Contador animado para estatísticas
    const counters = document.querySelectorAll('.stat-item h2');
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.textContent.replace(/\D/g, ''));
                const suffix = counter.textContent.replace(/\d/g, '');
                let current = 0;
                const increment = target / 100;
                
                const updateCounter = () => {
                    if (current < target) {
                        current += increment;
                        counter.textContent = Math.ceil(current) + suffix;
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target + suffix;
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
    
    // Melhorar experiência de navegação mobile
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Fechar menu ao clicar em um link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }
    
    // Prevenção de FOUC (Flash of Unstyled Content)
    document.body.classList.add('loaded');
    
    // Otimização de performance para scroll events
    let ticking = false;
    
    function updateOnScroll() {
        // Navbar scroll effect
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
        
        ticking = false;
    }
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateOnScroll);
            ticking = true;
        }
    });
    
    // Adicionar classe CSS para melhor controle de animações
    const style = document.createElement('style');
    style.textContent = `
        .navbar.scrolled {
            background-color: rgba(248, 249, 250, 0.98) !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .lazy {
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .lazy.loaded {
            opacity: 1;
        }
        
        body:not(.loaded) {
            opacity: 0;
        }
        
        body.loaded {
            opacity: 1;
            transition: opacity 0.3s ease-in;
        }
        
        .is-invalid {
            border-color: #dc3545 !important;
            animation: shake 0.5s ease-in-out;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);

    console.log("New Life website loaded successfully! 🌱");

    // Funcionalidade do modo escuro
    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");
    const body = document.body;

    // Verificar preferência salva ou preferência do sistema
    const savedTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    // Aplicar tema inicial
    if (savedTheme === "dark" || (!savedTheme && systemPrefersDark)) {
        enableDarkMode();
    } else {
        enableLightMode();
    }

    // Event listener para o toggle
    if (themeToggle) {
        themeToggle.addEventListener("click", function() {
            if (body.classList.contains("dark-mode")) {
                enableLightMode();
                localStorage.setItem("theme", "light");
            } else {
                enableDarkMode();
                localStorage.setItem("theme", "dark");
            }
        });
    }

    // Função para ativar modo escuro
    function enableDarkMode() {
        body.classList.add("dark-mode");
        if (themeIcon) {
            themeIcon.className = "fas fa-sun";
        }
        if (themeToggle) {
            themeToggle.title = "Alternar para modo claro";
        }

        // Atualizar meta theme-color para dispositivos móveis
        updateThemeColor("#1a1a1a");
    }

    // Função para ativar modo claro
    function enableLightMode() {
        body.classList.remove("dark-mode");
        if (themeIcon) {
            themeIcon.className = "fas fa-moon";
        }
        if (themeToggle) {
            themeToggle.title = "Alternar para modo escuro";
        }

        // Atualizar meta theme-color para dispositivos móveis
        updateThemeColor("#ffffff");
    }

    // Função para atualizar theme-color
    function updateThemeColor(color) {
        let themeColorMeta = document.querySelector("meta[name=\"theme-color\"]");
        if (!themeColorMeta) {
            themeColorMeta = document.createElement("meta");
            themeColorMeta.name = "theme-color";
            document.head.appendChild(themeColorMeta);
        }
        themeColorMeta.content = color;
    }

    // Escutar mudanças na preferência do sistema
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function(e) {
        if (!localStorage.getItem("theme")) {
            if (e.matches) {
                enableDarkMode();
            } else {
                enableLightMode();
            }
        }
    });

    // Adicionar animação suave ao alternar tema
    function addThemeTransition() {
        const style = document.createElement("style");
        style.textContent = `
            * {
                transition: background-color 0.3s ease, 
                           color 0.3s ease, 
                           border-color 0.3s ease,
                           box-shadow 0.3s ease !important;
            }
        `;
        document.head.appendChild(style);

        // Remover após a transição para não afetar outras animações
        setTimeout(() => {
            style.remove();
        }, 300);
    }

    // Aplicar transição ao alternar tema
    if (themeToggle) {
        themeToggle.addEventListener("click", addThemeTransition);
    }

    // Melhorar acessibilidade - permitir toggle com teclado
    if (themeToggle) {
        themeToggle.addEventListener("keydown", function(e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                this.click();
            }
        });
    }

    // Debug info
    console.log("Modo escuro implementado com sucesso! 🌙");
    console.log("Tema atual:", body.classList.contains("dark-mode") ? "Escuro" : "Claro");
});