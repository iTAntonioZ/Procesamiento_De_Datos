
import { supabase } from "./supabase.js";

const form = document.getElementById("auth-form");
const message = document.getElementById("message");
const password = document.getElementById("password");

// MOSTRAR Y OCULTAR CONTRASEÑA

document.querySelectorAll(".toggle").forEach(button => {
    button.addEventListener("click", () => {

        const input = document.getElementById(
            button.dataset.target
        );

        if (!input) return;

        const visible = input.type === "password";

        input.type = visible ? "text" : "password";

        button.textContent = visible
            ? "Ocultar"
            : "Mostrar";

        button.setAttribute("aria-pressed", String(visible));
    });
});

// AUTENTICACIÓN

form.addEventListener("submit", async event => {

    event.preventDefault();

    const modo = form.dataset.mode;

    const email = document
        .getElementById("email")
        .value.trim();

    const boton = form.querySelector(
        'button[type="submit"]'
    );

    boton.disabled = true;
    message.textContent = "Procesando...";

    try {

        // INICIO DE SESIÓN

        if (modo === "login") {

            const { error } =
                await supabase.auth.signInWithPassword({
                    email,
                    password: password.value
                });

            if (error) {
                throw new Error(
                    "Credenciales incorrectas o correo sin confirmar."
                );
            }

            message.textContent = "Sesión iniciada correctamente.";

            window.location.replace("dashboard.html");

            return;
        }

        // REGISTRO DE USUARIO

        if (modo === "registro" || modo === "register") {

            const nombre = document
                .getElementById("nombre")
                .value.trim();

            const confirmar = document
                .getElementById("confirmar")
                .value;

            if (!nombre) {
                throw new Error("Introduce tu nombre.");
            }

            if (password.value.length < 12) {
                throw new Error(
                    "La contraseña debe tener al menos 12 caracteres."
                );
            }

            if (password.value !== confirmar) {
                throw new Error(
                    "Las contraseñas no coinciden."
                );
            }

            const { data, error } =
                await supabase.auth.signUp({

                    email,

                    password: password.value,

                    options: {
                        data: { nombre },

                        emailRedirectTo: new URL(
                            "login.html",
                            window.location.href
                        ).href
                    }
                });

           if (error) {
    console.error("Error de Supabase:", error);

    throw new Error(
        "Error de registro: " + error.message
    );
}

            if (data.session) {

                window.location.replace("dashboard.html");

                return;
            }

            message.textContent =
                "Si el registro es válido, recibirás un correo de confirmación.";

            form.reset();

            return;
        }

        // RECUPERACIÓN DE CONTRASEÑA

        message.textContent =
            "La recuperación de contraseña se habilitará en la siguiente etapa.";

    } catch (error) {

        message.textContent = error.message;

    } finally {

        boton.disabled = false;
    }
});
