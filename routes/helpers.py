"""
helpers.py — Fonctions utilitaires partagées entre blueprints
Contributeur : Timothée
"""
import hashlib
from functools import wraps
from datetime import datetime
from flask import session, redirect, url_for, flash


def hash_mdp(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Connectez-vous pour accéder à cette page.", "warning")
            return redirect(url_for("auth.connexion"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Accès réservé aux administrateurs.", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated
