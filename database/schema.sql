CREATE TABLE IF NOT EXISTS utilisateur (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nom              TEXT    NOT NULL,
    prenom           TEXT    NOT NULL,
    email            TEXT    UNIQUE NOT NULL,
    mdp_hash         TEXT    NOT NULL,
    role             TEXT    NOT NULL DEFAULT 'user',
    date_inscription TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_utilisateur_email ON utilisateur(email);

CREATE TABLE IF NOT EXISTS matiere (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nom  TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ressource (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    titre          TEXT    NOT NULL,
    description    TEXT,
    lien_url       TEXT    NOT NULL,
    matiere_id     INTEGER REFERENCES matiere(id) ON DELETE SET NULL,
    promotion      TEXT,
    date_ajout     TEXT    NOT NULL,
    utilisateur_id INTEGER NOT NULL REFERENCES utilisateur(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ressource_matiere     ON ressource(matiere_id);
CREATE INDEX IF NOT EXISTS idx_ressource_utilisateur ON ressource(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_ressource_date        ON ressource(date_ajout);
