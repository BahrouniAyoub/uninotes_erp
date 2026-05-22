# UniNotes ERP

Mini projet Django — Framework Python pour le Web

## Fonctionnalités

- Authentification Django
- Rôles étudiant / tuteur
- Panier d’inscription
- Limite de 60 points
- Dashboard étudiant
- Gestion des notes
- Moyennes pondérées avec ORM Django
- Courbe d’évolution
- Dashboard tuteur en lecture seule
- Interface responsive

## Technologies

- Python
- Django
- SQLite
- HTML/CSS
- Chart.js

## Installation

```bash
git clone https://github.com/BahrouniAyoub/uninotes_erp.git
cd uninotes_erp
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver