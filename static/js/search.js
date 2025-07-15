document.addEventListener("DOMContentLoaded", function () {
    const productSearchInput = document.getElementById("search-input");
    const navbarSearchInput = document.getElementById("navbar-search-input");
    const navbarSearchButton = document.getElementById("navbar-search-button");
    const productCardsContainer = document.querySelector(".row.g-4"); // Container dos cards de produto

    // Função para filtrar produtos na página de categoria
    function filterProducts() {
        const searchTerm = productSearchInput.value.toLowerCase();
        const productCards = productCardsContainer ? productCardsContainer.querySelectorAll(".col-lg-4.col-md-6") : [];

        productCards.forEach(col => {
            const productName = col.querySelector(".card-title").textContent.toLowerCase();
            if (productName.includes(searchTerm)) {
                col.style.display = "";
            } else {
                col.style.display = "none";
            }
        });
    }

    // Lógica para a barra de pesquisa na página de produtos_categoria.html
    if (productSearchInput && productCardsContainer) {
        // Preencher o campo de pesquisa se houver um termo na URL
        const urlParams = new URLSearchParams(window.location.search);
        const searchTermFromUrl = urlParams.get("q");
        if (searchTermFromUrl) {
            productSearchInput.value = searchTermFromUrl;
            filterProducts(); // Filtrar imediatamente ao carregar a página
        }

        productSearchInput.addEventListener("keyup", filterProducts);
    }

    // Lógica para a barra de pesquisa na navbar (Enter)
    if (navbarSearchInput) {
        navbarSearchInput.addEventListener("keyup", function (event) {
            if (event.key === "Enter") {
                const searchTerm = navbarSearchInput.value;
                if (searchTerm) {
                    window.location.href = `/produtos/todos/?q=${encodeURIComponent(searchTerm)}`;
                } else {
                    window.location.href = `/produtos/todos/`;
                }
            }
        });
    }

    // Lógica para a lupa da navbar (Click)
    if (navbarSearchButton && navbarSearchInput) {
        navbarSearchButton.addEventListener("click", function () {
            const searchTerm = navbarSearchInput.value;
            if (searchTerm) {
                window.location.href = `/produtos/todos/?q=${encodeURIComponent(searchTerm)}`;
            } else {
                window.location.href = `/produtos/todos/`;
            }
        });
    }
});
