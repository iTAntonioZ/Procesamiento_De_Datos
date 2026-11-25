import { API } from "./api.js?v=4";

const $ = id => document.getElementById(id);


const estado = {

    datos: [],
    originales: [],
    archivo: null,
    actividad: [],
    rendimiento: [],
    ocupado: false
};


const algoritmos = [

    "Bubble Sort",
    "Selection Sort",
    "Insertion Sort",
    "Shell Sort",
    "Quick Sort",
    "Merge Sort",
    "Radix Sort",
    "Heap Sort"
];


const muestra = [

    42, 15, 8, 23, 4,
    16, 15, 9, 42, 2,
    7, 18, 36, 12, 27,
    32, 6, 21, 11, 28
];


const nombresPaginas = {

    dashboard: "Dashboard",
    datasets: "Datasets",
    ordenamientos: "Ordenamientos",
    busquedas: "Busquedas",
    externo: "Ordenamiento externo",
    rendimiento: "Rendimiento",
    seguridad: "Centro de seguridad",
    integridad: "Integridad SHA-256",
    auditoria: "Auditoria",
    exportaciones: "Exportaciones"
};


// ========================================
// NAVEGACION
// ========================================

function navegar(pagina) {

    document.querySelectorAll(".page")
        .forEach(seccion => {

            seccion.classList.toggle(
                "active",
                seccion.id === pagina
            );
        });

    document.querySelectorAll("[data-page]")
        .forEach(boton => {

            boton.classList.toggle(
                "active",
                boton.dataset.page === pagina
            );
        });

    $("breadcrumb-page").textContent =
        nombresPaginas[pagina] || pagina;

    $("sidebar").classList.remove("open");

    window.scrollTo(0, 0);
}


document.querySelectorAll("[data-page]")
    .forEach(boton => {

        boton.addEventListener("click", () => {

            navegar(boton.dataset.page);
        });
    });


document.querySelectorAll("[data-go]")
    .forEach(boton => {

        boton.addEventListener("click", () => {

            navegar(boton.dataset.go);
        });
    });


$("menu-toggle").addEventListener("click", () => {

    $("sidebar").classList.toggle("open");
});


// ========================================
// NOTIFICACIONES
// ========================================

let temporizador;


function notificar(mensaje) {

    const toast = $("toast");

    toast.textContent = mensaje;

    toast.classList.add("show");

    clearTimeout(temporizador);

    temporizador = setTimeout(() => {

        toast.classList.remove("show");

    }, 4000);
}


function segundos(tiempo) {

    return `${Number(tiempo).toFixed(6)} s`;
}


function crearElemento(etiqueta, texto, clase) {

    const elemento = document.createElement(etiqueta);

    if (texto !== undefined) {
        elemento.textContent = texto;
    }

    if (clase) {
        elemento.className = clase;
    }

    return elemento;
}


// ========================================
// CONTROL DE EJECUCIONES
// ========================================

async function ejecutar(boton, funcion) {

    if (estado.ocupado) {

        notificar("Hay una operacion en proceso.");

        return;
    }

    estado.ocupado = true;

    boton.disabled = true;

    try {

        await funcion();

    } catch (error) {

        notificar(error.message);

        registrarActividad(
            "Error de procesamiento",
            "Error"
        );

    } finally {

        boton.disabled = false;

        estado.ocupado = false;
    }
}


// ========================================
// AUDITORIA LOCAL
// ========================================

function registrarActividad(
    evento,
    resultado = "Correcto"
) {

    estado.actividad.unshift({

        fecha: new Date().toLocaleString(),

        evento,

        resultado
    });

    estado.actividad =
        estado.actividad.slice(0, 100);

    actualizarAuditoria();
}


function actualizarAuditoria() {

    const tabla = $("tabla-auditoria");

    const reciente = $("actividad-reciente");

    tabla.replaceChildren();

    reciente.replaceChildren();

    estado.actividad.forEach(actividad => {

        const fila = document.createElement("tr");

        [
            actividad.fecha,
            actividad.evento,
            actividad.resultado

        ].forEach(valor => {

            fila.appendChild(
                crearElemento("td", valor)
            );
        });

        tabla.appendChild(fila);
    });

    estado.actividad.slice(0, 5)
        .forEach(actividad => {

            reciente.appendChild(

                crearElemento(
                    "p",
                    `${actividad.fecha} — ${actividad.evento}`
                )
            );
        });

    if (!estado.actividad.length) {

        reciente.textContent =
            "No hay actividad registrada.";
    }
}


// ========================================
// VISUALIZACION
// ========================================

function actualizarDatos(posiciones = []) {

    $("total-registros").textContent =
        estado.datos.length.toLocaleString();

    const vista = $("vista-datos");

    vista.replaceChildren();

    if (!estado.datos.length) {

        vista.textContent = "No hay datos cargados.";

        actualizarGrafica();

        return;
    }

    const coincidencias = new Set(posiciones);

    estado.datos.slice(0, 50)
        .forEach((numero, indice) => {

            const celda = crearElemento(
                "div",
                numero,
                "number-cell"
            );

            celda.title = `Posicion ${indice + 1}`;

            if (coincidencias.has(indice + 1)) {

                celda.classList.add("highlight");
            }

            vista.appendChild(celda);
        });

    actualizarGrafica();
}


function actualizarGrafica() {

    const grafica = $("grafica-datos");

    grafica.replaceChildren();

    const datos = estado.datos.slice(0, 40);

    if (!datos.length) {

        grafica.textContent = "Carga un dataset.";

        return;
    }

    const maximo = Math.max(
        1,
        ...datos.map(numero => Math.abs(numero))
    );

    datos.forEach(numero => {

        const barra = crearElemento(
            "div",
            "",
            "data-bar"
        );

        barra.style.height =
            `${Math.max(4, Math.abs(numero) / maximo * 180)}px`;

        barra.title = String(numero);

        grafica.appendChild(barra);
    });
}


function establecerDatos(datos, archivo) {

    estado.datos = [...datos];

    estado.originales = [...datos];

    estado.archivo = archivo;

    estado.rendimiento = [];

    $("resultado-ordenamiento").textContent =
        "Esperando ejecucion.";

    $("resultado-busqueda").textContent =
        "Esperando busqueda.";

    actualizarDatos();

    actualizarRendimiento();
}


// ========================================
// CARGA DE DATASETS REALES
// ========================================

document.querySelectorAll("[data-dataset]")
    .forEach(boton => {

        boton.addEventListener("click", () => {

            ejecutar(boton, async () => {

                notificar("Cargando dataset desde Python...");

                const resultado =
                    await API.cargarDataset(
                        boton.dataset.dataset
                    );

                establecerDatos(
                    resultado.datos,
                    resultado.archivo
                );

                registrarActividad(
                    `Dataset cargado: ${resultado.archivo}`
                );

                notificar(
                    `${resultado.cantidad} registros cargados en ` +
                    segundos(resultado.tiempo)
                );
            });
        });
    });


$("cargar-muestra").addEventListener("click", () => {

    if (estado.ocupado) return;

    establecerDatos(muestra, "Muestra");

    registrarActividad("Datos de prueba cargados");

    notificar("Datos de prueba cargados.");
});


$("limpiar-datos").addEventListener("click", () => {

    if (estado.ocupado) return;

    establecerDatos([], null);

    registrarActividad("Datos eliminados");

    notificar("Datos eliminados.");
});


// ========================================
// ORDENAMIENTOS INTERNOS
// ========================================

$("ejecutar-ordenamiento")
    .addEventListener("click", function () {

        ejecutar(this, async () => {

            if (!estado.datos.length) {

                throw new Error("Carga un dataset primero.");
            }

            const algoritmo = $("algoritmo").value;

            const orden = $("orden").value;

            notificar(`Ejecutando ${algoritmo}...`);

            const resultado = await API.ordenar(

                estado.datos,
                algoritmo,
                orden
            );

            estado.datos = resultado.datos;

            actualizarDatos();

            $("resultado-ordenamiento").textContent =

                `Algoritmo: ${resultado.algoritmo}\n` +
                `Orden: ${resultado.orden}\n` +
                `Registros: ${resultado.cantidad}\n` +
                `Tiempo: ${segundos(resultado.tiempo)}\n\n` +
                `Primeros 20:\n` +
                resultado.datos.slice(0, 20).join(", ") +
                `\n\nUltimos 20:\n` +
                resultado.datos.slice(-20).join(", ");

            registrarActividad(
                `Ordenamiento: ${resultado.algoritmo}`
            );

            notificar("Ordenamiento completado por Python.");
        });
    });


// ========================================
// BUSQUEDAS
// ========================================

$("ejecutar-busqueda")
    .addEventListener("click", function () {

        ejecutar(this, async () => {

            if (!estado.datos.length) {

                throw new Error("Carga un dataset primero.");
            }

            const entrada = $("valor-busqueda").value;

            const valor = Number(entrada);

            if (
                entrada.trim() === "" ||
                !Number.isSafeInteger(valor)
            ) {

                throw new Error("Introduce un entero valido.");
            }

            const metodo = $("metodo-busqueda").value;

            const resultado = await API.buscar(

                estado.datos,
                metodo,
                valor
            );

            $("resultado-busqueda").textContent =

                `Metodo: ${resultado.metodo}\n` +
                `Valor: ${resultado.valor}\n` +
                `Coincidencias: ${resultado.coincidencias}\n` +
                `Tiempo: ${segundos(resultado.tiempo)}\n` +
                `Preparacion: ${segundos(resultado.tiempo_preparacion)}\n` +
                `Indice: ${segundos(resultado.tiempo_indice)}\n\n` +
                `Posiciones:\n` +
                (
                    resultado.posiciones.length
                        ? resultado.posiciones.join(", ")
                        : "No encontrado"
                );

            actualizarDatos(resultado.posiciones);

            registrarActividad(
                `Busqueda ${metodo}: ${valor}`
            );

            notificar(
                `${resultado.coincidencias} coincidencias.`
            );
        });
    });


// ========================================
// ORDENAMIENTO EXTERNO
// ========================================

$("calcular-bloques")
    .addEventListener("click", function () {

        ejecutar(this, async () => {

            const formato =
                $("dataset-externo").value === "1000"
                    ? "txt"
                    : "xlsx";

            const bloque = Number(
                $("tamano-bloque").value
            );

            if (
                !Number.isInteger(bloque) ||
                bloque < 1 ||
                bloque > 5000
            ) {

                throw new Error("Tamano de bloque invalido.");
            }

            notificar("Ejecutando ordenamiento externo...");

            const resultado = await API.externo(

                formato,
                bloque,
                $("orden-externo").value
            );

            const contenedor = $("bloques");

            contenedor.replaceChildren();

            for (
                let i = 0;
                i < Math.min(resultado.bloques, 50);
                i++
            ) {

                contenedor.appendChild(

                    crearElemento(
                        "div",
                        `Bloque ${i + 1}`,
                        "number-cell"
                    )
                );
            }

            $("resultado-externo").textContent =

                `Algoritmo: ${resultado.algoritmo}\n` +
                `Orden: ${resultado.orden}\n` +
                `Registros: ${resultado.cantidad}\n` +
                `Bloques: ${resultado.bloques}\n` +
                `Pasadas: ${resultado.pasadas}\n` +
                `Tiempo: ${segundos(resultado.tiempo)}\n\n` +
                `Primeros 20:\n` +
                resultado.datos.slice(0, 20).join(", ");

            estado.datos = resultado.datos;

            estado.archivo = formato === "txt"
                ? "dataset_1000_duplicados.txt"
                : "dataset_5000_duplicados.xlsx";

            // Recuperar el original para futuras comparaciones.
            estado.originales = [];

            estado.rendimiento = [];

            actualizarDatos();

            actualizarRendimiento();

            registrarActividad("Ordenamiento externo completado");

            notificar("Ordenamiento externo finalizado.");
        });
    });


// ========================================
// RENDIMIENTO
// ========================================

function actualizarRendimiento() {

    const tabla = $("tabla-rendimiento");

    const grafica = $("grafica-rendimiento");

    tabla.replaceChildren();

    grafica.replaceChildren();

    algoritmos.forEach(algoritmo => {

        const resultado = estado.rendimiento.find(

            item => item.algoritmo === algoritmo
        );

        const fila = document.createElement("tr");

        const valores = [

            algoritmo,

            resultado ? resultado.cantidad : "—",

            resultado
                ? segundos(resultado.tiempo)
                : "Sin medir",

            resultado ? "Completado" : "Pendiente"
        ];

        valores.forEach(valor => {

            fila.appendChild(
                crearElemento("td", valor)
            );
        });

        tabla.appendChild(fila);
    });

    if (!estado.rendimiento.length) {

        grafica.textContent = "Sin mediciones todavia.";

        return;
    }

    const maximo = Math.max(

        0.000000001,

        ...estado.rendimiento.map(item => item.tiempo)
    );

    estado.rendimiento.forEach(item => {

        const barra = crearElemento(
            "div",
            "",
            "data-bar"
        );

        barra.style.height =
            `${Math.max(4, item.tiempo / maximo * 180)}px`;

        barra.title =
            `${item.algoritmo}: ${segundos(item.tiempo)}`;

        grafica.appendChild(barra);
    });
}


$("comparar-algoritmos")
    .addEventListener("click", function () {

        ejecutar(this, async () => {

            if (!estado.datos.length) {

                throw new Error("Carga un dataset primero.");
            }

            let originales = estado.originales;

            if (!originales.length) {

                const formato =
                    estado.archivo.endsWith(".xlsx")
                        ? "xlsx"
                        : "txt";

                const original =
                    await API.cargarDataset(formato);

                originales = original.datos;

                estado.originales = [...originales];
            }

            notificar("Comparando los ocho algoritmos...");

            const respuesta = await API.rendimiento(

                originales,
                $("orden").value
            );

            estado.rendimiento = respuesta.resultados;

            actualizarRendimiento();

            registrarActividad(
                "Comparacion de rendimiento completada"
            );

            notificar("Comparacion finalizada.");
        });
    });


// ========================================
// CENTRO DE SEGURIDAD
// ========================================

function actualizarSeguridad() {

    const contenedor = $("controles-seguridad");

    contenedor.replaceChildren();

    const controles = [

        [
            "Autenticacion",
            "Supabase Auth y validacion de tokens en Python."
        ],

        [
            "Control de acceso",
            "Endpoints de procesamiento autenticados."
        ],

        [
            "Integridad",
            "Calculo criptografico SHA-256."
        ],

        [
            "Validacion de datos",
            "Tipos, formatos y limites de registros."
        ],

        [
            "Rate Limiting",
            "Limite local de peticiones al backend."
        ],

        [
            "Seguridad HTTP",
            "Cabeceras de proteccion configuradas."
        ],

        [
            "Auditoria",
            "Registro local. Persistencia pendiente."
        ],

        [
            "Base de datos",
            "Politicas RLS pendientes de verificacion."
        ],

        [
            "HTTPS",
            "Pendiente de publicacion."
        ]
    ];

    controles.forEach(([nombre, descripcion]) => {

        const tarjeta = crearElemento(
            "div",
            undefined,
            "panel"
        );

        tarjeta.appendChild(
            crearElemento("h3", nombre)
        );

        tarjeta.appendChild(
            crearElemento("p", descripcion)
        );

        contenedor.appendChild(tarjeta);
    });
}


// ========================================
// INTEGRIDAD SHA-256
// ========================================

$("calcular-hash")
    .addEventListener("click", function () {

        ejecutar(this, async () => {

            const archivo =
                $("archivo-integridad").files[0];

            if (!archivo) {

                throw new Error("Selecciona un archivo.");
            }

            if (!/\.(txt|xlsx)$/i.test(archivo.name)) {

                throw new Error("Formato no permitido.");
            }

            if (archivo.size > 5 * 1024 * 1024) {

                throw new Error("Limite de archivo: 5 MB.");
            }

            const referencia = $("hash-referencia")
                .value.trim().toLowerCase();

            if (
                referencia &&
                !/^[a-f0-9]{64}$/.test(referencia)
            ) {

                throw new Error("Hash de referencia invalido.");
            }

            const contenido = await archivo.arrayBuffer();

            const digest = await crypto.subtle.digest(
                "SHA-256",
                contenido
            );

            const hash = Array.from(
                new Uint8Array(digest)
            ).map(
                byte => byte.toString(16).padStart(2, "0")
            ).join("");

            const resultado = !referencia

                ? "Sin hash de referencia"

                : hash === referencia

                    ? "Los hashes coinciden"

                    : "Los hashes no coinciden";

            $("resultado-hash").textContent =

                `Archivo: ${archivo.name}\n\n` +
                `SHA-256:\n${hash}\n\n` +
                `Resultado: ${resultado}`;

            registrarActividad(
                `Verificacion SHA-256: ${archivo.name}`,
                referencia && hash !== referencia
                    ? "Advertencia"
                    : "Correcto"
            );

            notificar("Hash calculado.");
        });
    });


// ========================================
// EXPORTACIONES
// ========================================

async function exportar(formato) {

    if (!estado.datos.length) {

        throw new Error("No hay datos para exportar.");
    }

    const archivo = await API.exportar(

        estado.datos,
        formato
    );

    const url = URL.createObjectURL(archivo);

    const enlace = document.createElement("a");

    enlace.href = url;

    enlace.download = `resultado.${formato}`;

    document.body.appendChild(enlace);

    enlace.click();

    enlace.remove();

    setTimeout(() => URL.revokeObjectURL(url), 1000);

    registrarActividad(
        `Exportacion ${formato.toUpperCase()}`
    );

    notificar("Archivo generado por Python.");
}


$("exportar-txt").addEventListener("click", function () {

    ejecutar(this, () => exportar("txt"));
});


$("exportar-xlsx").addEventListener("click", function () {

    ejecutar(this, () => exportar("xlsx"));
});


// ========================================
// INICIALIZACION
// ========================================

actualizarDatos();

actualizarRendimiento();

actualizarSeguridad();

actualizarAuditoria();
