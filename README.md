# Projet-Green-IT
# BiblioLibre

Plateforme collaborative de partage de ressources pédagogiques éco-conçue.
Projet Numérique Durable
EFREI Paris 2025/2026.

**URL déployée :** https://bibliolibre.onrender.com 

## Équipe

| Membre | Rôle |
|---|---|
| Timothée | Chef de projet, architecture |
| Enzo | Back-end authentification | 
| Louis | Back-end ressources |
| Lilia | Front-end, CSS, layout |
| Rayane | Back-end admin & profil |

## Stack technique

| Composant | Choix | Justification Green IT |
|---|---|---|
| Front-end | HTML5 + CSS3 natif | Zéro framework JS, pages < 200 Ko |
| Back-end | Python / Flask | Micro-framework, < 5 dépendances |
| Base de données | SQLite | Zéro serveur dédié, empreinte minimale |
| Hébergement | Render.com | Plan gratuit, HTTPS inclus |
| Polices | Système (`system-ui`) | Zéro requête externe |

## Lancer en local

```bash
# 1. Cloner le dépôt
git clone https://github.com/RayaneBsr/Projet-Green-IT.git
cd Projet-Green-IT

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Copier le fichier d'environnement
cp .env.example .env

# 5. Initialiser la base de données
python init_db.py

# 6. Lancer le serveur
python app.py
```

Ouvrir **http://localhost:5000**

## Compte démo

| Email | Mot de passe | Rôle |
|---|---|---|
| admin@bibliolibre.fr | admin1234 | Administrateur |

## Structure du dépôt

```
bibliolibre/
├── app.py                          # Factory Flask, route index
├── init_db.py                      # Initialisation BDD
├── requirements.txt
├── .env.example
├── .gitignore
├── database/
│   └── schema.sql                  # Schéma SQL
├── routes/
│   ├── helpers.py                  # Décorateurs login_required, hash_mdp…
│   ├── auth.py                     # Inscription, connexion, déconnexion
│   ├── ressources.py               # CRUD ressources
│   ├── admin.py                    # Admin utilisateurs
│   └── profil.py                   # Profil utilisateur
├── static/
│   └── style.css                   # Feuille de style unique
├── templates/
│   ├── base.html                   # Layout commun
│   ├── index.html                  # Page d'accueil
│   ├── profil.html                 # Profil utilisateur
│   ├── auth/
│   │   ├── connexion.html
│   │   └── inscription.html
│   ├── ressources/
│   │   ├── liste.html
│   │   └── form.html
│   └── admin/
│       ├── utilisateurs.html
│       └── modifier_user.html
└── docs/                           # Rapport
```


## Principes Green IT appliqués

- Pages < 200 Ko (HTML + CSS uniquement, 1 fichier CSS, 0 JS)
- Police système (`system-ui`) — zéro requête externe
- Filtres via formulaire GET natif — fonctionnent sans JavaScript
- SQLite — zéro serveur dédié, schéma normalisé 3NF
- Aucun fichier binaire stocké — liens URL uniquement
- Pagination serveur (LIMIT/OFFSET) — pas de scroll infini
