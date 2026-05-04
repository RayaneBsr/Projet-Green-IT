"""
routes/profil.py — Gestion du profil utilisateur
Contributeur : Rayane
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db
from routes.helpers import login_required, hash_mdp

bp = Blueprint("profil", __name__)


@bp.route("/profil", methods=["GET", "POST"])
@login_required
def profil():
    db = get_db()
    u  = db.execute(
        "SELECT id, nom, prenom, email, role, date_inscription FROM utilisateur WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    mes_ressources = db.execute("""
        SELECT r.id, r.titre, r.date_ajout, r.lien_url, m.nom AS matiere_nom
        FROM ressource r
        LEFT JOIN matiere m ON r.matiere_id = m.id
        WHERE r.utilisateur_id = ?
        ORDER BY r.date_ajout DESC
    """, (session["user_id"],)).fetchall()

    if request.method == "POST":
        prenom = request.form.get("prenom", "").strip()
        nom    = request.form.get("nom", "").strip()
        email  = request.form.get("email", "").strip().lower()
        mdp    = request.form.get("mdp", "")

        if not all([prenom, nom, email]):
            flash("Prénom, nom et email sont obligatoires.", "error")
            return render_template("profil.html", u=u, mes_ressources=mes_ressources)

        existant = db.execute(
            "SELECT id FROM utilisateur WHERE email = ? AND id != ?",
            (email, session["user_id"])
        ).fetchone()
        if existant:
            flash("Cet email est déjà utilisé.", "error")
            return render_template("profil.html", u=u, mes_ressources=mes_ressources)

        if mdp:
            if len(mdp) < 8:
                flash("Mot de passe trop court (8 caractères min.).", "error")
                return render_template("profil.html", u=u, mes_ressources=mes_ressources)
            db.execute(
                "UPDATE utilisateur SET nom=?, prenom=?, email=?, mdp_hash=? WHERE id=?",
                (nom, prenom, email, hash_mdp(mdp), session["user_id"])
            )
        else:
            db.execute(
                "UPDATE utilisateur SET nom=?, prenom=?, email=? WHERE id=?",
                (nom, prenom, email, session["user_id"])
            )

        db.commit()
        session["user_nom"] = prenom
        flash("Profil mis à jour.", "success")
        return redirect(url_for("profil.profil"))

    return render_template("profil.html", u=u, mes_ressources=mes_ressources)


@bp.route("/profil/supprimer", methods=["POST"])
@login_required
def supprimer():
    uid = session["user_id"]
    db  = get_db()
    db.execute("DELETE FROM utilisateur WHERE id = ?", (uid,))
    db.commit()
    session.clear()
    flash("Votre compte a été supprimé.", "success")
    return redirect(url_for("index"))
