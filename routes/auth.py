from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db
from routes.helpers import hash_mdp, now_str

bp = Blueprint("auth", __name__)


@bp.route("/connexion", methods=["GET", "POST"])
def connexion():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        mdp   = request.form.get("mdp", "")

        if not email or not mdp:
            flash("Email et mot de passe requis.", "error")
            return render_template("auth/connexion.html")

        db = get_db()
        u  = db.execute(
            "SELECT id, nom, prenom, mdp_hash, role FROM utilisateur WHERE email = ?",
            (email,)
        ).fetchone()

        if u and u["mdp_hash"] == hash_mdp(mdp):
            session.clear()
            session["user_id"]  = u["id"]
            session["user_nom"] = u["prenom"]
            session["role"]     = u["role"]
            flash(f"Bienvenue, {u['prenom']} !", "success")
            return redirect(request.args.get("next") or url_for("index"))

        flash("Email ou mot de passe incorrect.", "error")

    return render_template("auth/connexion.html")


@bp.route("/inscription", methods=["GET", "POST"])
def inscription():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        prenom = request.form.get("prenom", "").strip()
        nom    = request.form.get("nom", "").strip()
        email  = request.form.get("email", "").strip().lower()
        mdp    = request.form.get("mdp", "")
        mdp2   = request.form.get("mdp2", "")

        erreur = None
        if not all([prenom, nom, email, mdp, mdp2]):
            erreur = "Tous les champs sont obligatoires."
        elif "@" not in email or "." not in email:
            erreur = "Format d'email invalide."
        elif mdp != mdp2:
            erreur = "Les mots de passe ne correspondent pas."
        elif len(mdp) < 8:
            erreur = "Le mot de passe doit contenir au moins 8 caractères."

        if erreur:
            flash(erreur, "error")
            return render_template("auth/inscription.html",
                                   prenom=prenom, nom=nom, email=email)

        db = get_db()
        if db.execute("SELECT 1 FROM utilisateur WHERE email = ?", (email,)).fetchone():
            flash("Cet email est déjà utilisé.", "error")
            return render_template("auth/inscription.html",
                                   prenom=prenom, nom=nom, email=email)

        db.execute("""
            INSERT INTO utilisateur (nom, prenom, email, mdp_hash, role, date_inscription)
            VALUES (?, ?, ?, ?, 'user', ?)
        """, (nom, prenom, email, hash_mdp(mdp), now_str()))
        db.commit()

        flash("Compte créé avec succès. Connectez-vous.", "success")
        return redirect(url_for("auth.connexion"))

    return render_template("auth/inscription.html", prenom="", nom="", email="")


@bp.route("/deconnexion")
def deconnexion():
    session.clear()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("index"))
