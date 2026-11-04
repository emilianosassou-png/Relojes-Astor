const buscador = document.getElementById("buscador");
const filtroCategoria = document.getElementById("filtroCategoria");
const productos = document.querySelectorAll(".product-card");


function filtrarProductos() {

    const texto = buscador.value.toLowerCase();
    const categoria = filtroCategoria.value;

    productos.forEach(producto => {

        const nombre = producto.dataset.nombre;
        const marca = producto.dataset.marca;
        const categoriaProducto = producto.dataset.categoria;

        const coincideTexto =
            nombre.includes(texto) ||
            marca.includes(texto);

        const coincideCategoria =
            categoria === "todos" ||
            categoriaProducto === categoria;

        if (coincideTexto && coincideCategoria) {

            producto.style.display = "block";

        } else {

            producto.style.display = "none";

        }

    });
}


if (buscador) {
    buscador.addEventListener(
        "input",
        filtrarProductos
    );
}


if (filtroCategoria) {
    filtroCategoria.addEventListener(
        "change",
        filtrarProductos
    );
}


function confirmarEliminacion() {

    return confirm(
        "¿Estás seguro de que querés eliminar este reloj?"
    );

}


function abrirEditar(
    id,
    nombre,
    marca,
    precio,
    stock,
    categoria,
    descripcion,
    imagen
) {

    const modal =
        document.getElementById("modalEditar");

    const formulario =
        document.getElementById("formEditar");

    formulario.action = "/editar/" + id;

    document.getElementById(
        "editarNombre"
    ).value = nombre;

    document.getElementById(
        "editarMarca"
    ).value = marca;

    document.getElementById(
        "editarPrecio"
    ).value = precio;

    document.getElementById(
        "editarStock"
    ).value = stock;

    document.getElementById(
        "editarCategoria"
    ).value = categoria;

    document.getElementById(
        "editarDescripcion"
    ).value = descripcion;

    const vistaPrevia = document.getElementById("editarVistaPrevia");
    const entradaImagen = document.getElementById("editarImagen");
    entradaImagen.value = "";
    vistaPrevia.src = imagen;
    vistaPrevia.hidden = !imagen;

    modal.style.display = "flex";
}

document.getElementById("editarImagen").addEventListener("change", function() {
    const vistaPrevia = document.getElementById("editarVistaPrevia");
    const archivo = this.files[0];

    if (archivo) {
        vistaPrevia.src = URL.createObjectURL(archivo);
        vistaPrevia.hidden = false;
    }
});


function cerrarEditar() {

    document.getElementById(
        "modalEditar"
    ).style.display = "none";

}


window.addEventListener("click", function(event) {

    const modal =
        document.getElementById("modalEditar");

    if (event.target === modal) {
        cerrarEditar();
    }

});