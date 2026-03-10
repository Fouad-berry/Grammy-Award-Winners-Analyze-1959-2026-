# Grammy Award Winners Analyzer (1959–2026)

Projet d'analyse, visualisation et Machine Learning sur les Grammy Awards.

## Structure du projet

```
dataset/           # Contient le fichier grammy_awards.csv
python/            # Scripts d'analyse et de ML
api/               # API FastAPI
frontend/          # Dashboard Next.js
requirements.txt   # Dépendances Python
```

## Prérequis
- Python 3.8+
- (Optionnel) Node.js pour le frontend

## Installation rapide

1. **Cloner le repo**

```bash
git clone https://github.com/Fouad-berry/Grammy-Award-Winners-Analyze-1959-2026-.git
cd Grammy-Award-Winners-Analyze-1959-2026-
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. **Installer les dépendances Python**

```bash
pip install -r requirements.txt
```

4. **Placer le fichier `grammy_awards.csv` dans le dossier `dataset/`**

5. **Lancer l'analyse**

```bash
python python/analysis.py
```

6. **Lancer l'API**

```bash
uvicorn api.main:app --reload
```

7. **Frontend (optionnel)**

Voir le dossier `frontend/` pour le dashboard Next.js.

---

## Fonctionnalités prévues
- Statistiques et visualisations sur les Grammy Awards
- Analyse par artiste, genre, décennie
- Machine Learning (clustering, prédiction)
- API REST pour exposer les analyses
- Dashboard interactif

---

## Auteurs
- Fouad Berry

---

## TODO
