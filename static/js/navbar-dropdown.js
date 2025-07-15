// Correção específica para dropdown mobile - New Life
// Este script garante que o dropdown funcione corretamente em dispositivos móveis

document.addEventListener('DOMContentLoaded', function() {
    
    // Função para detectar se estamos em dispositivo móvel
    function isMobile() {
        return window.innerWidth < 992; // Bootstrap lg breakpoint
    }
    
    // Obter elementos necessários
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const dropdownToggles = document.querySelectorAll('.navbar-nav .dropdown-toggle');
    
    if (!navbarCollapse || dropdownToggles.length === 0) {
        return; // Sair se não encontrar os elementos
    }
    
    // Função para fechar todos os dropdowns
    function closeAllDropdowns() {
        const openDropdowns = navbarCollapse.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(menu => {
            menu.classList.remove('show');
            const toggle = menu.previousElementSibling;
            if (toggle && toggle.classList.contains('dropdown-toggle')) {
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    // Função para toggle de um dropdown específico
    function toggleDropdown(toggle, dropdownMenu) {
        const isOpen = dropdownMenu.classList.contains('show');
        
        if (isOpen) {
            // Fechar este dropdown
            dropdownMenu.classList.remove('show');
            toggle.setAttribute('aria-expanded', 'false');
        } else {
            // Fechar outros dropdowns primeiro
            closeAllDropdowns();
            
            // Abrir este dropdown
            dropdownMenu.classList.add('show');
            toggle.setAttribute('aria-expanded', 'true');
        }
    }
    
    // Adicionar event listeners para cada dropdown toggle
    dropdownToggles.forEach(toggle => {
        const dropdownMenu = toggle.nextElementSibling;
        
        if (!dropdownMenu || !dropdownMenu.classList.contains('dropdown-menu')) {
            return; // Pular se não encontrar o menu dropdown
        }
        
        // Event listener para clique
        toggle.addEventListener('click', function(e) {
            if (isMobile()) {
                // Em mobile, prevenir comportamento padrão e controlar manualmente
                e.preventDefault();
                e.stopPropagation();
                toggleDropdown(toggle, dropdownMenu);
            }
            // Em desktop, deixar o Bootstrap controlar
        });
        
        // Event listener para teclado (acessibilidade)
        toggle.addEventListener('keydown', function(e) {
            if (isMobile() && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault();
                e.stopPropagation();
                toggleDropdown(toggle, dropdownMenu);
            }
        });
    });
    
    // Fechar dropdowns quando clicar fora (apenas em mobile)
    document.addEventListener('click', function(e) {
        if (isMobile()) {
            // Verificar se o clique foi fora da navbar
            if (!navbarCollapse.contains(e.target)) {
                closeAllDropdowns();
            }
        }
    });
    
    // Fechar dropdowns quando redimensionar a janela para desktop
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            closeAllDropdowns();
        }
    });
    
    // Fechar dropdowns quando o menu navbar for fechado
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            // Pequeno delay para aguardar o Bootstrap processar
            setTimeout(() => {
                if (!navbarCollapse.classList.contains('show')) {
                    closeAllDropdowns();
                }
            }, 100);
        });
    }
    
    // Melhorar comportamento dos itens do dropdown
    const dropdownItems = navbarCollapse.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            // Fechar o menu navbar após clicar em um item (apenas em mobile)
            if (isMobile() && navbarToggler) {
                setTimeout(() => {
                    if (navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                }, 100);
            }
        });
    });
    
    // Debug: Log para verificar se o script está funcionando
    console.log('Dropdown mobile fix carregado com sucesso!');
    console.log('Dropdowns encontrados:', dropdownToggles.length);
    
    // Função para debug (pode ser removida em produção)
    window.debugDropdown = function() {
        console.log('Estado atual dos dropdowns:');
        dropdownToggles.forEach((toggle, index) => {
            const menu = toggle.nextElementSibling;
            console.log(`Dropdown ${index + 1}:`, {
                toggle: toggle.textContent.trim(),
                isOpen: menu ? menu.classList.contains('show') : 'Menu não encontrado',
                ariaExpanded: toggle.getAttribute('aria-expanded')
            });
        });
    };
});

// Adicionar estilos CSS dinâmicos para melhorar a experiência
const dynamicStyles = document.createElement('style');
dynamicStyles.textContent = `
    /* Melhorar feedback visual durante interação */
    @media (max-width: 991.98px) {
        .navbar-nav .dropdown-toggle:active {
            background-color: rgba(0,0,0,0.05);
            border-radius: 4px;
        }
        
        .dark-mode .navbar-nav .dropdown-toggle:active {
            background-color: rgba(255,255,255,0.1);
        }
        
        /* Garantir que a transição seja suave */
        .navbar-nav .dropdown-menu {
            transition: all 0.3s ease;
        }
        
        .navbar-nav .dropdown-menu.show {
            animation: slideDown 0.3s ease-out;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Melhorar área de toque */
        .navbar-nav .dropdown-toggle,
        .navbar-nav .dropdown-item {
            -webkit-tap-highlight-color: rgba(0,0,0,0.1);
        }
        
        .dark-mode .navbar-nav .dropdown-toggle,
        .dark-mode .navbar-nav .dropdown-item {
            -webkit-tap-highlight-color: rgba(255,255,255,0.1);
        }
    }
`;

// Adicionar os estilos ao head
document.head.appendChild(dynamicStyles);

