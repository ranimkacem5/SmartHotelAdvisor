import json
from unidecode import unidecode


def clean_text(text):
    """Corrige l'encodage et supprime espaces inutiles."""
    text = unidecode(text)  # enlève les caractères mal encodés
    text = text.replace("  ", " ")  # supprime espaces doublons
    return text.strip()


def process_json(raw_data):
    """Nettoie et restructure le JSON brut en format Python-ready."""
    documents = []
    id_counter = 1

    for item in raw_data:
        url = item.get("url")
        title = clean_text(item.get("title", ""))
        images = item.get("images", [])

        # 🟢 Nettoyer paragraphes et supprimer doublons
        paragraphs = []
        seen = set()
        for c in item.get("content", []):
            p = clean_text(c.get("paragraph", ""))
            if p and p not in seen:
                paragraphs.append(p)
                seen.add(p)

        # 🟢 Fusionner paragraphes
        full_text = " ".join(paragraphs)

        # 🟢 Déterminer la catégorie depuis le titre (single, double, triple)
        category = "other"
        if "single" in title.lower():
            category = "single"
        elif "double" in title.lower():
            category = "double"
        elif "triple" in title.lower():
            category = "triple"

        # 🟢 Ajouter document nettoyé
        documents.append({
            "id": f"room_{category}_{id_counter}",
            "title": title,
            "text": full_text,
            "url": url,
            "category": category,
            "images": images
        })
        id_counter += 1

    return documents


# Lire ton JSON brut
with open("scraped_content.csv", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Nettoyer et restructurer
cleaned_docs = process_json(raw_data)

# Sauvegarder le JSON prêt pour RAG
with open("clean_data.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_docs, f, indent=2, ensure_ascii=False)
