# Étape 1 : image de base
FROM python:3.10-slim

# Étape 2 : définir le répertoire de travail
WORKDIR /app

# Étape 3 : copier les fichiers nécessaires
COPY scraper.py .
COPY soussanahotel_links.json .
COPY requirements.txt .

# Étape 4 : installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : définir le point d'entrée
CMD ["python", "scraper.py"]
