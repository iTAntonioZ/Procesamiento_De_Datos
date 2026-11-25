
import { supabase } from "./supabase.js";

// ========================================
// CONEXION CON EL BACKEND PYTHON
// ========================================

async function peticion(
    ruta,
    metodo = "GET",
    datos = null,
    descargar = false
) {

    const { data, error } =
        await supabase.auth.getSession();

    if (error || !data.session) {

        window.location.replace("login.html");

        throw new Error("Inicia sesion nuevamente.");
    }

    const opciones = {

        method: metodo,

        headers: {
            "Content-Type": "application/json",
            "Authorization":
                `Bearer ${data.session.access_token}`
        },

        cache: "no-store"
    };

    if (datos !== null) {
        opciones.body = JSON.stringify(datos);
    }

    const respuesta = await fetch(
        `/api${ruta}`,
        opciones
    );

    if (respuesta.status === 401) {

        throw new Error(
            "No se pudo validar tu sesion."
        );
    }

    if (!respuesta.ok) {

        const resultado = await respuesta.json()
            .catch(() => ({}));

        throw new Error(
            resultado.error ||
            `Error del servidor: ${respuesta.status}`
        );
    }

    if (descargar) {
        return respuesta.blob();
    }

    return respuesta.json();
}


// ========================================
// FUNCIONES DE LA API
// ========================================

export const API = {

    // CARGAR DATASET

    cargarDataset(formato) {

        return peticion(
            `/datasets/${formato}`
        );
    },


    // ORDENAMIENTO INTERNO

    ordenar(datos, algoritmo, orden) {

        return peticion(
            "/ordenar",
            "POST",
            {
                datos,
                algoritmo,
                orden
            }
        );
    },


    // METODOS DE BUSQUEDA

    buscar(datos, metodo, valor) {

        return peticion(
            "/buscar",
            "POST",
            {
                datos,
                metodo,
                valor
            }
        );
    },


    // ORDENAMIENTO EXTERNO

    externo(formato, bloque, orden = "asc") {

        return peticion(
            "/externo",
            "POST",
            {
                formato,
                bloque,
                orden
            }
        );
    },


    // COMPARACION DE RENDIMIENTO

    rendimiento(datos, orden = "asc") {

        return peticion(
            "/rendimiento",
            "POST",
            {
                datos,
                orden
            }
        );
    },


    // EXPORTACION TXT Y XLSX

    exportar(datos, formato) {

        return peticion(
            "/exportar",
            "POST",
            {
                datos,
                formato
            },
            true
        );
    }
};
