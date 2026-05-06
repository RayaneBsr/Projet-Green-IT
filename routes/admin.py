from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db
from routes.helpers import login_required, admin_required, hash_mdp

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/utilisateurs")
@login_required
@admin_required
def utilisateurs():
    db    = get_db()
    users = db.execute("""
        SELECT u.id, u.nom, u.prenom, u.email, u.role, u.date_inscription,
               COUNT(r.id) AS nb_ressources
        FROM utilisateur u
        LEFT JOIN ressource r ON r.utilisateur_id = u.id
        GROUP BY u.id
        ORDER BY u.date_inscription DESC
    """).fetchall()
    return render_template("admin/utilisateurs.html", users=users)


@bp.route("/utilisateurs/<int:uid>/modifier", methods=["GET", "POST"])
@login_required
@admin_required
def modifier_user(uid):
    db = get_db()
    u  = db.execute(
        "SELECT id, nom, prenom, email, role FROM utilisateur WHERE id = ?", (uid,)
    ).fetchone()

    if not u:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("admin.utilisateurs"))

    if request.method == "POST":
        prenom = request.form.get("prenom", "").strip()
        nom    = request.form.get("nom", "").strip()
        email  = request.form.get("email", "").strip().lower()
        role   = request.form.get("role", "user")
        mdp    = request.form.get("mdp", "")

        if not all([prenom, nom, email]):
            flash("Prénom, nom et email sont obligatoires.", "error")
            return render_template("admin/modifier_user.html", u=u)

        existant = db.execute(
            "SELECT id FROM utilisateur WHERE email = ? AND id != ?", (email, uid)
        ).fetchone()
        if existant:
            flash("Cet email est déjà utilisé.", "error")
            return render_template("admin/modifier_user.html", u=u)

        if mdp:
            if len(mdp) < 8:
                flash("Mot de passe trop court (8 caractères min.).", "error")
                return render_template("admin/modifier_user.html", u=u)
            db.execute(
                "UPDATE utilisateur SET nom=?, prenom=?, email=?, role=?, mdp_hash=? WHERE id=?",
                (nom, prenom, email, role, hash_mdp(mdp), uid)
            )
        else:
            db.execute(
                "UPDATE utilisateur SET nom=?, prenom=?, email=?, role=? WHERE id=?",
                (nom, prenom, email, role, uid)
            )

        db.commit()
        flash("Utilisateur mis à jour.", "success")
        return redirect(url_for("admin.utilisateurs"))

    return render_template("admin/modifier_user.html", u=u)


@bp.route("/utilisateurs/<int:uid>/supprimer", methods=["POST"])
@login_required
@admin_required
def supprimer_user(uid):
    if uid == session.get("user_id"):
        flash("Impossible de supprimer votre propre compte.", "error")
        return redirect(url_for("admin.utilisateurs"))

    db = get_db()
    if not db.execute("SELECT 1 FROM utilisateur WHERE id = ?", (uid,)).fetchone():
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("admin.utilisateurs"))

    db.execute("DELETE FROM utilisateur WHERE id = ?", (uid,))
    db.commit()
    flash("Utilisateur supprimé.", "success")
    return redirect(url_for("admin.utilisateurs"))
