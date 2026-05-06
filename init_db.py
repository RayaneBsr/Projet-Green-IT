import sqlite3
import hashlib
import os
from datetime import datetime


def hash_mdp(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()


def init_db(db_path=None):
    if db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), "database", "bibliolibre.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    with open(os.path.join(os.path.dirname(__file__), "database", "schema.sql"), "r") as f:
        conn.executescript(f.read())

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Matières
    matieres = [
        ("Recherche Opérationnelle",   "RO"),
        ("Cloud Computing",            "CC"),
        ("Bases de données",           "BDD"),
        ("VHDL",                       "VHDL"),
        ("Théorie du signal",          "TDS"),
        ("Numérique durable",          "ND"),
        ("Théorie de graphes",         "TDG"),
        ("Systeme de transimission",   "SDT"),
        ("Français",                   "FR"),
        ("Anglais",                    "ANG"),
    ]
    for nom, code in matieres:
        conn.execute(
            "INSERT OR IGNORE INTO matiere (nom, code) VALUES (?, ?)",
            (nom, code)
        )

    # Compte admin par défaut
    conn.execute("""
        INSERT OR IGNORE INTO utilisateur
            (nom, prenom, email, mdp_hash, role, date_inscription)
        VALUES ('Admin', 'BiblioLibre', 'admin@bibliolibre.fr', ?, 'admin', ?)
    """, (hash_mdp("admin1234"), now))

    admin = conn.execute(
        "SELECT id FROM utilisateur WHERE email='admin@bibliolibre.fr'"
    ).fetchone()

    if admin:
        aid = admin["id"]
        demos = [
            ("Résumé Fourier & Laplace",
             "Synthèse des transformées pour l'examen final",
             "https://example.com/fourier", 5, "I3"),
            ("Annales BD 2024 — corrigées",
             "Toutes les annales avec solutions détaillées",
             "https://example.com/bdd", 3, "I2"),
            ("Fiche mémo Floyd-Warshall",
             "Algorithme pas à pas avec exemples tracés",
             "https://example.com/floyd", 2, "I3"),
            ("Intro aux réseaux — couche OSI",
             "Cours complet modèle OSI, TCP/IP et routage",
             "https://example.com/reseaux", 4, "P1"),
            ("Guide TPs Numérique Durable",
             "Méthodologie et ressources pour les TPs TI616",
             "https://example.com/ti616", 6, "I3"),
        ]
        for titre, desc, lien, mid, promo in demos:
            conn.execute("""
                INSERT OR IGNORE INTO ressource
                    (titre, description, lien_url, matiere_id, promotion,
                     date_ajout, utilisateur_id)
                SELECT ?,?,?,?,?,?,?
                WHERE NOT EXISTS (SELECT 1 FROM ressource WHERE titre=?)
            """, (titre, desc, lien, mid, promo, now, aid, titre))

    conn.commit()
    conn.close()
    print(f"Base de données initialisée : {db_path}")


if __name__ == "__main__":
    init_db()
