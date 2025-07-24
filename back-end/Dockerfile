# Étape 1 : Utiliser une image Python légère
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Étape 7 : Exposer le port de l'application Flask
EXPOSE 5000


CMD ["python", "app.py"]



