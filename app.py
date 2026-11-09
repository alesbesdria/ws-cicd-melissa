
import os
import socket
import psycopg

from flask import Flask, jsonify

app = Flask(__name__)

# Message affiché sur la page d'accueil
MESSAGE = "C'est GoooooooooooooDDDDDDDDDD !!!!!!!"

# Version injectée au build
VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/")
def index():
    return (
        f"<h1>{MESSAGE}</h1>"
        f"<p>Version : <code>{VERSION[:7]}</code></p>"
        f"<p>Conteneur : <code>{socket.gethostname()}</code></p>"
    )


@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION)


@app.route("/db")
def database_check():
    try:
        with psycopg.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            sslmode="require",
            connect_timeout=5
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return jsonify(
            status="connected",
            database="PostgreSQL Azure",
            message="Connexion à la base de données réussie"
        ), 200

    except Exception:
        app.logger.exception("Erreur de connexion PostgreSQL")
        return jsonify(
            status="error",
            message="Connexion à PostgreSQL impossible"
        ), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
