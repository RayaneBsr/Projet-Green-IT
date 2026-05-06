import os
import sqlite3
from flask import Flask, g, session, render_template

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "bibliolibre.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    app.config["DB_PATH"] = DB_PATH

    app.teardown_appcontext(close_db)

    @app.context_processor
    def inject_user():
        return {
            "current_user_id":   session.get("user_id"),
            "current_user_nom":  session.get("user_nom"),
            "current_user_role": session.get("role"),
        }

    from routes.auth       import bp as auth_bp
    from routes.ressources import bp as ressources_bp
    from routes.admin      import bp as admin_bp
    from routes.profil     import bp as profil_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ressources_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profil_bp)

    @app.route("/")
    def index():
        db = get_db()
        recentes = db.execute("""
            SELECT r.id, r.titre, r.description, r.lien_url, r.date_ajout,
                   r.promotion, m.nom AS matiere_nom,
                   u.prenom || ' ' || u.nom AS auteur
            FROM ressource r
            LEFT JOIN matiere m ON r.matiere_id = m.id
            JOIN utilisateur u ON r.utilisateur_id = u.id
            ORDER BY r.date_ajout DESC LIMIT 8
        """).fetchall()
        stats = db.execute("""
            SELECT
              (SELECT COUNT(*) FROM ressource)                     AS nb_ressources,
              (SELECT COUNT(*) FROM utilisateur WHERE role='user') AS nb_contributeurs,
              (SELECT COUNT(*) FROM matiere)                       AS nb_matieres
        """).fetchone()
        return render_template("index.html", recentes=recentes, stats=stats)

    return app


if __name__ == "__main__":
    from init_db import init_db
    init_db(DB_PATH)
    app = create_app()
    app.run(debug=True, port=5000)
