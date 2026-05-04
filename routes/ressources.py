"""
routes/ressources.py — CRUD ressources pédagogiques
Contributeur : Louis
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db
from routes.helpers import login_required, now_str

bp = Blueprint("ressources", __name__)

PROMOTIONS = ["P1", "P2", "I1", "I2", "I3"]
PAR_PAGE   = 15


@bp.route("/ressources")
def liste():
    db         = get_db()
    matiere_id = request.args.get("matiere", "").strip()
    promotion  = request.args.get("promotion", "").strip()
    q          = request.args.get("q", "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1

    where, params = ["1=1"], []
    if matiere_id:
        where.append("r.matiere_id = ?")
        params.append(matiere_id)
    if promotion:
        where.append("r.promotion = ?")
        params.append(promotion)
    if q:
        where.append("(r.titre LIKE ? OR r.description LIKE ?)")
        params += [f"%{q}%", f"%{q}%"]

    clause = " AND ".join(where)
    total  = db.execute(
        f"SELECT COUNT(*) FROM ressource r WHERE {clause}", params
    ).fetchone()[0]

    nb_pages = max(1, (total + PAR_PAGE - 1) // PAR_PAGE)
    page     = min(page, nb_pages)
    offset   = (page - 1) * PAR_PAGE

    items = db.execute(f"""
        SELECT r.id, r.titre, r.description, r.lien_url,
               r.date_ajout, r.promotion, r.utilisateur_id,
               m.nom AS matiere_nom,
               u.prenom || ' ' || u.nom AS auteur
        FROM ressource r
        LEFT JOIN matiere m ON r.matiere_id = m.id
        JOIN utilisateur u ON r.utilisateur_id = u.id
        WHERE {clause}
        ORDER BY r.date_ajout DESC
        LIMIT ? OFFSET ?
    """, params + [PAR_PAGE, offset]).fetchall()

    matieres = db.execute("SELECT id, nom FROM matiere ORDER BY nom").fetchall()

    return render_template("ressources/liste.html",
        items=items, matieres=matieres, promotions=PROMOTIONS,
        filtre_matiere=matiere_id, filtre_promo=promotion, q=q,
        page=page, nb_pages=nb_pages, total=total)


@bp.route("/ressources/creer", methods=["GET", "POST"])
@login_required
def creer():
    db       = get_db()
    matieres = db.execute("SELECT id, nom FROM matiere ORDER BY nom").fetchall()

    if request.method == "POST":
        titre      = request.form.get("titre", "").strip()
        description= request.form.get("description", "").strip()
        lien_url   = request.form.get("lien_url", "").strip()
        matiere_id = request.form.get("matiere_id") or None
        promotion  = request.form.get("promotion") or None

        if not titre:
            flash("Le titre est obligatoire.", "error")
        elif not lien_url:
            flash("Le lien URL est obligatoire.", "error")
        elif not lien_url.startswith(("http://", "https://")):
            flash("Le lien doit commencer par http:// ou https://", "error")
        else:
            db.execute("""
                INSERT INTO ressource
                    (titre, description, lien_url, matiere_id, promotion,
                     date_ajout, utilisateur_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (titre, description, lien_url, matiere_id, promotion,
                  now_str(), session["user_id"]))
            db.commit()
            flash("Ressource ajoutée.", "success")
            return redirect(url_for("ressources.liste"))

    return render_template("ressources/form.html",
                           matieres=matieres, promotions=PROMOTIONS,
                           ressource=None, action="Déposer")


@bp.route("/ressources/<int:rid>/modifier", methods=["GET", "POST"])
@login_required
def modifier(rid):
    db = get_db()
    r  = db.execute("SELECT * FROM ressource WHERE id = ?", (rid,)).fetchone()

    if not r:
        flash("Ressource introuvable.", "error")
        return redirect(url_for("ressources.liste"))
    if r["utilisateur_id"] != session["user_id"] and session.get("role") != "admin":
        flash("Vous ne pouvez modifier que vos propres ressources.", "error")
        return redirect(url_for("ressources.liste"))

    matieres = db.execute("SELECT id, nom FROM matiere ORDER BY nom").fetchall()

    if request.method == "POST":
        titre      = request.form.get("titre", "").strip()
        description= request.form.get("description", "").strip()
        lien_url   = request.form.get("lien_url", "").strip()
        matiere_id = request.form.get("matiere_id") or None
        promotion  = request.form.get("promotion") or None

        if not titre or not lien_url:
            flash("Titre et lien URL sont obligatoires.", "error")
        elif not lien_url.startswith(("http://", "https://")):
            flash("Le lien doit commencer par http:// ou https://", "error")
        else:
            db.execute("""
                UPDATE ressource
                SET titre=?, description=?, lien_url=?,
                    matiere_id=?, promotion=?
                WHERE id=?
            """, (titre, description, lien_url, matiere_id, promotion, rid))
            db.commit()
            flash("Ressource mise à jour.", "success")
            return redirect(url_for("ressources.liste"))

    return render_template("ressources/form.html",
                           matieres=matieres, promotions=PROMOTIONS,
                           ressource=r, action="Modifier")


@bp.route("/ressources/<int:rid>/supprimer", methods=["POST"])
@login_required
def supprimer(rid):
    db = get_db()
    r  = db.execute(
        "SELECT utilisateur_id FROM ressource WHERE id = ?", (rid,)
    ).fetchone()

    if not r:
        flash("Ressource introuvable.", "error")
    elif r["utilisateur_id"] != session["user_id"] and session.get("role") != "admin":
        flash("Action non autorisée.", "error")
    else:
        db.execute("DELETE FROM ressource WHERE id = ?", (rid,))
        db.commit()
        flash("Ressource supprimée.", "success")

    return redirect(url_for("ressources.liste"))
