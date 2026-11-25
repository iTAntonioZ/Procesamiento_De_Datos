import sqlite3

from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "instance" / "dataprocess.db"


@contextmanager
def conectar():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row

    try:
        conexion.execute("PRAGMA foreign_keys = ON")
        yield conexion
        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def inicializar_db():

    with conectar() as db:

        db.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'usuario',
                fecha_registro DATETIME
                    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                evento TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
            );
        """)


if __name__ == "__main__":
    inicializar_db()
    print("Base de datos inicializada correctamente.")