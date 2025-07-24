# Étape 1 : Utiliser une image Python légère
FROM python:3.10-slim

# Étape 2 : Créer le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers de dépendances
COPY requirements.txt .

# Étape 4 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le reste du code dans le conteneur
COPY . .

# Étape 6 : Exposer le port utilisé par Flask ou FastAPI
EXPOSE 5000

# Étape 7 : Définir la commande de démarrage
CMD ["python", "app.py"]
