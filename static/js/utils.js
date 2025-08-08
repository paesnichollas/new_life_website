/**
 * Utilitários JavaScript para New Life Website
 */

// =============================================================================
// UTILITÁRIOS GERAIS
// =============================================================================

/**
 * Debounce function para otimizar performance
 * @param {Function} func - Função a ser executada
 * @param {number} wait - Tempo de espera em ms
 * @returns {Function} - Função debounced
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function para limitar execução
 * @param {Function} func - Função a ser executada
 * @param {number} limit - Limite de execução em ms
 * @returns {Function} - Função throttled
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

/**
 * Verifica se elemento está visível na viewport
 * @param {Element} element - Elemento a verificar
 * @returns {boolean} - True se visível
 */
function isElementInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Formata número para moeda brasileira
 * @param {number} value - Valor a formatar
 * @returns {string} - Valor formatado
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Formata data para formato brasileiro
 * @param {string|Date} date - Data a formatar
 * @returns {string} - Data formatada
 */
function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('pt-BR');
}

// =============================================================================
// UTILITÁRIOS DE NOTIFICAÇÃO
// =============================================================================

/**
 * Exibe notificação toast
 * @param {string} message - Mensagem a exibir
 * @param {string} type - Tipo da notificação (success, error, warning, info)
 * @param {number} duration - Duração em ms
 */
function showToast(message, type = 'info', duration = 3000) {
    // Remover toasts existentes
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());

    // Criar toast
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Adicionar ao DOM
    document.body.appendChild(toast);

    // Animar entrada
    setTimeout(() => toast.classList.add('show'), 100);

    // Remover automaticamente
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Exibe loading spinner
 * @param {string} message - Mensagem opcional
 */
function showLoading(message = 'Carregando...') {
    const loading = document.createElement('div');
    loading.id = 'loading-overlay';
    loading.innerHTML = `
        <div class="loading-content">
            <div class="spinner-newlife"></div>
            <p class="loading-message">${message}</p>
        </div>
    `;
    document.body.appendChild(loading);
}

/**
 * Remove loading spinner
 */
function hideLoading() {
    const loading = document.getElementById('loading-overlay');
    if (loading) {
        loading.remove();
    }
}

// =============================================================================
// UTILITÁRIOS DE FORMULÁRIO
// =============================================================================

/**
 * Valida email
 * @param {string} email - Email a validar
 * @returns {boolean} - True se válido
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Valida CPF
 * @param {string} cpf - CPF a validar
 * @returns {boolean} - True se válido
 */
function validateCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    
    if (cpf.length !== 11) return false;
    
    // Verificar dígitos repetidos
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    // Validar primeiro dígito verificador
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let digit = 11 - (sum % 11);
    if (digit > 9) digit = 0;
    if (parseInt(cpf.charAt(9)) !== digit) return false;
    
    // Validar segundo dígito verificador
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    digit = 11 - (sum % 11);
    if (digit > 9) digit = 0;
    if (parseInt(cpf.charAt(10)) !== digit) return false;
    
    return true;
}

/**
 * Formata CPF
 * @param {string} cpf - CPF a formatar
 * @returns {string} - CPF formatado
 */
function formatCPF(cpf) {
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

/**
 * Formata telefone
 * @param {string} phone - Telefone a formatar
 * @returns {string} - Telefone formatado
 */
function formatPhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{2})(\d{4,5})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

// =============================================================================
// UTILITÁRIOS DE LOCAL STORAGE
// =============================================================================

/**
 * Salva item no localStorage
 * @param {string} key - Chave
 * @param {any} value - Valor
 */
function saveToStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error('Erro ao salvar no localStorage:', e);
    }
}

/**
 * Recupera item do localStorage
 * @param {string} key - Chave
 * @param {any} defaultValue - Valor padrão
 * @returns {any} - Valor recuperado
 */
function getFromStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
        console.error('Erro ao recuperar do localStorage:', e);
        return defaultValue;
    }
}

/**
 * Remove item do localStorage
 * @param {string} key - Chave
 */
function removeFromStorage(key) {
    try {
        localStorage.removeItem(key);
    } catch (e) {
        console.error('Erro ao remover do localStorage:', e);
    }
}

// =============================================================================
// UTILITÁRIOS DE REQUISIÇÃO
// =============================================================================

/**
 * Faz requisição AJAX
 * @param {string} url - URL da requisição
 * @param {Object} options - Opções da requisição
 * @returns {Promise} - Promise da requisição
 */
async function fetchAPI(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };

    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        return await response.text();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

/**
 * Faz requisição POST
 * @param {string} url - URL da requisição
 * @param {Object} data - Dados a enviar
 * @returns {Promise} - Promise da requisição
 */
async function postAPI(url, data) {
    return fetchAPI(url, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

/**
 * Faz requisição GET
 * @param {string} url - URL da requisição
 * @returns {Promise} - Promise da requisição
 */
async function getAPI(url) {
    return fetchAPI(url, {
        method: 'GET'
    });
}

// =============================================================================
// UTILITÁRIOS DE ANIMAÇÃO
// =============================================================================

/**
 * Anima elemento com fade in
 * @param {Element} element - Elemento a animar
 * @param {number} duration - Duração em ms
 */
function fadeIn(element, duration = 300) {
    element.style.opacity = '0';
    element.style.display = 'block';
    
    let start = null;
    function animate(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const opacity = Math.min(progress / duration, 1);
        
        element.style.opacity = opacity;
        
        if (progress < duration) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

/**
 * Anima elemento com fade out
 * @param {Element} element - Elemento a animar
 * @param {number} duration - Duração em ms
 */
function fadeOut(element, duration = 300) {
    const startOpacity = parseFloat(getComputedStyle(element).opacity);
    let start = null;
    
    function animate(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const opacity = startOpacity * (1 - Math.min(progress / duration, 1));
        
        element.style.opacity = opacity;
        
        if (progress < duration) {
            requestAnimationFrame(animate);
        } else {
            element.style.display = 'none';
        }
    }
    
    requestAnimationFrame(animate);
}

// =============================================================================
// EXPORTAÇÃO DOS UTILITÁRIOS
// =============================================================================

// Tornar funções disponíveis globalmente
window.NewLifeUtils = {
    debounce,
    throttle,
    isElementInViewport,
    formatCurrency,
    formatDate,
    showToast,
    showLoading,
    hideLoading,
    validateEmail,
    validateCPF,
    formatCPF,
    formatPhone,
    saveToStorage,
    getFromStorage,
    removeFromStorage,
    fetchAPI,
    postAPI,
    getAPI,
    fadeIn,
    fadeOut
};

// Exportar para módulos (se suportado)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.NewLifeUtils;
}
