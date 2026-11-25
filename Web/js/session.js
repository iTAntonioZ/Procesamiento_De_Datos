
import { supabase } from "./supabase.js";

async function verificarSesion() {

    const { data, error } =
        await supabase.auth.getUser();

    if (error || !data.user) {

        window.location.replace("login.html");

        return;
    }

    const usuario = data.user;

    const nombre =
        usuario.user_metadata?.nombre ||
        usuario.email ||
        "Usuario";

    const avatar = document.querySelector(".avatar");

    const etiqueta = document.querySelector(
        ".user-area .muted"
    );

    if (avatar) {
        avatar.textContent = nombre
            .slice(0, 2)
            .toUpperCase();
    }

    if (etiqueta) {
        etiqueta.textContent = nombre;
    }

    const logout = document.querySelector(".logout");

    if (logout) {

        logout.textContent = "Cerrar sesión";

        logout.addEventListener("click", async event => {

            event.preventDefault();

            const { error } =
                await supabase.auth.signOut();

            if (error) {
                alert("No se pudo cerrar la sesión.");
                return;
            }

            window.location.replace("login.html");
        });
    }

    document.body.style.visibility = "visible";
}

verificarSesion();
