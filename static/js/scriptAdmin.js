function saveRow(id) {
    var row = document.getElementById('row-' + id);
    var cells = row.getElementsByClassName('editable');
    var data = {};

    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        data[cell.getAttribute('data-column')] = cell.innerText;
    }

    fetch('/edit_product/' + id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Producto actualizado exitosamente');
        } else {
            alert('Error al actualizar el producto');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const searchBox = document.getElementById("searchBox");
    const categoryFilter = document.getElementById("categoryFilter");

    searchBox.addEventListener("input", filterProducts);
    categoryFilter.addEventListener("change", filterProducts);

    function filterProducts() {
        const searchText = searchBox.value.toLowerCase();
        const selectedCategory = categoryFilter.value;
        const rows = document.querySelectorAll("table tr[id^='row-']");

        rows.forEach(row => {
            const productName = row.getAttribute("data-name");
            const productCategory = row.getAttribute("data-category");

            const nameMatches = productName.includes(searchText);
            const categoryMatches = selectedCategory === "" || productCategory === selectedCategory;

            if (nameMatches && categoryMatches) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }
});
