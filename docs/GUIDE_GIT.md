# Guide Git — BiblioLibre

Guide rapide pour contribuer au projet depuis ton poste.
A lire une fois, garder sous la main pour les commits.

---

## 1. Installation et configuration (a faire une seule fois)

Verifier que Git est installe :
```bash
git --version
```

Configurer ton identite (utilise le meme nom que sur GitHub) :
```bash
git config --global user.name "Ton Prenom Nom"
git config --global user.email "ton.email@exemple.com"
```

---

## 2. Recuperer le projet

```bash
git clone https://github.com/RayaneBsr/Projet-Green-IT.git
cd Projet-Green-IT
```

---

## 3. Creer ta branche

Chaque membre travaille sur sa propre branche. Ne jamais travailler directement sur `main`.

```bash
git checkout -b feature/ton-prenom
```

Exemples :
```bash
git checkout -b feature/timothee   # Timothee
git checkout -b feature/enzo       # Enzo
git checkout -b feature/lilia      # Lilia
git checkout -b feature/louis      # Louis
git checkout -b feature/rayane     # Rayane
```

---

## 4. Copier tes fichiers

Copie les fichiers de ton zip dans le dossier du projet en respectant l'arborescence.

Exemple pour Enzo :
```
Projet-Green-IT/
  routes/auth.py              <-- coller ici
  templates/auth/connexion.html
  templates/auth/inscription.html
```

---

## 5. Faire un commit

```bash
# Voir les fichiers modifies / ajoutes
git status

# Ajouter tes fichiers
git add routes/auth.py
git add templates/auth/

# Ou tout ajouter d'un coup (si tu es sur de tes fichiers)
git add .

# Creer le commit avec un message clair
git commit -m "feat: ajout de l'authentification (Enzo)"
```

---

## 6. Pousser ta branche sur GitHub

```bash
git push origin feature/ton-prenom
```

La premiere fois Git te demandera tes identifiants GitHub.

---

## 7. Ouvrir une Pull Request (PR)

1. Aller sur https://github.com/RayaneBsr/Projet-Green-IT
2. GitHub affiche une banniere "Compare & pull request" sur ta branche
3. Cliquer dessus
4. Titre : `feat: contribution de [ton prenom]`
5. Cliquer sur "Create pull request"
6. Prevenir Timothee pour qu'il merge dans l'ordre

---

## Ordre de merge dans main

Respecter cet ordre pour eviter les conflits :

| Ordre | Membre | Branche |
|---|---|---|
| 1 | Timothee | feature/timothee |
| 2 | Lilia | feature/lilia |
| 3 | Enzo | feature/enzo |
| 4 | Louis | feature/louis |
| 5 | Rayane | feature/rayane |

---

## Commandes utiles

```bash
# Voir sur quelle branche tu es
git branch

# Voir l'historique des commits
git log --oneline

# Recuperer les derniers changements de main (apres un merge)
git checkout main
git pull origin main

# Revenir sur ta branche de travail
git checkout feature/ton-prenom

# Mettre a jour ta branche avec les derniers changements de main
git merge main
```

---

## Conventions de commit

Prefixe + description courte en francais :

```
feat: ajout d'une nouvelle fonctionnalite
fix: correction d'un bug
style: modification CSS ou mise en forme
docs: mise a jour de la documentation
db: modification du schema ou des donnees
```

---

## En cas de probleme

**"Your branch is behind main"**
```bash
git pull origin main
```

**Conflit de fusion**
Ouvrir le fichier en conflit, chercher les balises `<<<<<<<`, choisir la bonne version, puis :
```bash
git add fichier_en_conflit
git commit -m "fix: resolution conflit"
```

**Annuler le dernier commit (pas encore pousse)**
```bash
git reset --soft HEAD~1
```
