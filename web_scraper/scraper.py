import json
import time
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from unidecode import unidecode


# 🔹 Charger les URLs depuis un fichier JSON


def load_urls(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [entry["url"] for entry in data]

# 🔹 Scraper une page HTML


def scrape_page(url, image_folder="images"):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Erreur HTTP {response.status_code} pour {url}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "Sans titre"

        # 🔸 Associer chaque <h1>/<h2> à un <p> même dans des divs
        content = []
        for tag in soup.find_all(['h1', 'h2']):
            header_text = tag.get_text(strip=True)

            # Chercher le <p> suivant dans le flux HTML
            next_element = tag.find_next()
            while next_element and next_element != tag:
                if next_element.name == 'p':
                    paragraph_text = next_element.get_text(strip=True)
                    if paragraph_text:  # ignorer les <p> vides
                        content.append({
                            "header": header_text,
                            "paragraph": paragraph_text
                        })
                        break
                next_element = next_element.find_next()

        # 🔸 Récupérer les images
        img_tags = soup.find_all('img')
        img_urls = []

        domain = urlparse(url).netloc.replace(".", "_")
        page_folder = os.path.join(image_folder, domain)
        os.makedirs(page_folder, exist_ok=True)

        for img in img_tags:
            src = img.get('src')
            if src:
                full_url = urljoin(url, src)
                img_urls.append(full_url)

                try:
                    img_data = requests.get(full_url, timeout=10).content
                    img_name = os.path.basename(full_url.split("?")[0])
                    img_path = os.path.join(page_folder, img_name)
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                except Exception as e:
                    print(f"❌ Erreur image {full_url} : {e}")

        return {
            "url": url,
            "title": title,
            "content": content,
            "images": img_urls
        }

    except Exception as e:
        print(f"❌ Erreur scraping {url} : {e}")
        return None

# 🔹 Sauvegarde au format JSON


def save_to_json(data, filename="scraped_content.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 🔹 Fonction principale


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
        elif "family" in title.lower():
            category = "family"

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


def main():
    urls = load_urls("soussanahotel_links.json")
    print(f"📥 {len(urls)} URLs à scraper.\n")

    scraped_data = []
    for i, url in enumerate(urls, start=1):
        print(f"🔎 ({i}/{len(urls)}) Scraping : {url}")
        result = scrape_page(url)
        if result:
            scraped_data.append(result)
        time.sleep(1)  # Pause pour éviter de surcharger le site

    save_to_json(scraped_data)
    print("\n✅ Scraping terminé. Résultats enregistrés dans scraped_content.json")


with open("scraped_content.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Nettoyer et restructurer
cleaned_docs = process_json(raw_data)

# Sauvegarder le JSON prêt pour RAG
with open("clean_data.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_docs, f, indent=2, ensure_ascii=False)
# 🔹 Lancer le script
if __name__ == "__main__":
    main()
