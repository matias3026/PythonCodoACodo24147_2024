// -----------------------------para usar local----------------------------------
// ------------------------------------------------------------------------------


// Función para guardar una fila editada
function saveRow(id) {
    // Obtiene la fila específica por su ID
    var row = document.getElementById('row-' + id);
    
    // Obtiene todas las celdas editables dentro de la fila
    var cells = row.getElementsByClassName('editable');
    
    // Inicializa un objeto para almacenar los datos
    var data = {};

    // Recorre todas las celdas editables y almacena los datos en el objeto
    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        // Usa el atributo 'data-column' como clave y el texto de la celda como valor
        data[cell.getAttribute('data-column')] = cell.innerText;
    }

    // Envía una petición POST al servidor con los datos editados
    fetch('/edit_product/' + id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Especifica el tipo de contenido como JSON
        },
        body: JSON.stringify(data),  // Convierte el objeto de datos a una cadena JSON
    })
    .then(response => response.json())  // Convierte la respuesta del servidor a JSON
    .then(data => {
        // Muestra una alerta dependiendo del éxito o fallo de la operación
        if (data.success) {
            alert('Producto actualizado exitosamente');
        } else {
            alert('Error al actualizar el producto');
        }
    })
    .catch((error) => {
        // Maneja cualquier error que ocurra durante la petición
        console.error('Error:', error);
    });
}

// Espera a que el documento esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {
    // Obtiene el cuadro de búsqueda y el filtro de categoría
    const searchBox = document.getElementById("searchBox");
    const categoryFilter = document.getElementById("categoryFilter");

    // Añade eventos para el cuadro de búsqueda y el filtro de categoría
    searchBox.addEventListener("input", filterProducts);
    categoryFilter.addEventListener("change", filterProducts);

    // Función para filtrar productos basada en la búsqueda y la categoría seleccionada
    function filterProducts() {
        // Obtiene el texto de búsqueda en minúsculas
        const searchText = searchBox.value.toLowerCase();
        // Obtiene la categoría seleccionada
        const selectedCategory = categoryFilter.value;
        // Obtiene todas las filas de productos en la tabla
        const rows = document.querySelectorAll("table tr[id^='row-']");

        // Recorre cada fila de producto
        rows.forEach(row => {
            // Obtiene el nombre y la categoría del producto desde los atributos de la fila
            const productName = row.getAttribute("data-name");
            const productCategory = row.getAttribute("data-category");

            // Verifica si el nombre del producto incluye el texto de búsqueda
            const nameMatches = productName.includes(searchText);
            // Verifica si la categoría del producto coincide con la seleccionada (o si no se seleccionó ninguna categoría)
            const categoryMatches = selectedCategory === "" || productCategory === selectedCategory;

            // Muestra u oculta la fila según si ambas condiciones son verdaderas
            if (nameMatches && categoryMatches) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }
});
