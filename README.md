"# SmartHotelAdvisor"

Nom : Postgres Local



service : postgres\_db ()

host:db le nom du service dans ton docker-compose

Port : 5432



Username : admin



Password : admin









les étapes de mon projet sont :

✅ 1. Charger les URLs

Lit un fichier JSON (soussanahotel\_links.json) pour récupérer toutes les URLs à scraper.

✅ 2. Scraper chaque page

Télécharge le HTML.

Extrait :

Titre de la page.

Sections texte : pour chaque <h1> / <h2>, prend le premier paragraphe <p> qui suit.

Images : télécharge toutes les images et les enregistre dans un dossier images/.



✅ 3. Sauvegarder les données brutes

Enregistre tout ça dans un fichier scraped\_content.json.



✅ 4. Nettoyer et organiser les données

Supprime les doublons et caractères mal encodés.

Fusionne les paragraphes en un texte unique.

Détecte la catégorie (single, double, triple, family) d’après le titre.



✅ 5. Sauvegarder les données propres

Crée un fichier clean\_data.json prêt à être utilisé (ex. pour un chatbot ou un système RAG).



✅ 6. Automatisation

La fonction main() lance tout le processus :

➡️ Charger URLs → Scraper → Sauvegarder → Nettoyer → Exporter.

📌 En résumé :

➡️ Scrape le site → Télécharge textes et images → Nettoie et structure → Produit un JSON final exploitable.



les étapes suivantes :



1️⃣ Lecture des données nettoyées

On lit le fichier cleaned\_data.json (produit par clean\_data.py).

Chaque élément contient :

✅ un titre

✅ un texte (ex. description de la chambre, politique de l’hôtel, etc.)

✅ une URL ou une source



&nbsp;2️⃣ Création des embeddings

Pour chaque texte, on demande à OpenAI de créer un embedding :

Un embedding est un vecteur numérique (ex. 1536 dimensions pour text-embedding-3-small).

Ces vecteurs permettent à Chroma de faire de la recherche par similarité.



&nbsp;3️⃣ Stockage dans Chroma

On utilise Chroma comme base vectorielle.

Chaque document est stocké avec :

✅ Son embedding (le vecteur)

✅ Son contenu textuel

✅ Ses métadonnées (titre, URL)

