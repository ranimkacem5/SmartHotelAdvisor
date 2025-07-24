import json
import time
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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

        # 🔸 Associer chaque <h1>/<h2> à son <p> suivant
        content = []
        for tag in soup.find_all(['h1', 'h2']):
            header_text = tag.get_text(strip=True)
            next_p = tag.find_next_sibling()
            while next_p and next_p.name != 'p':
                next_p = next_p.find_next_sibling()
            if next_p:
                paragraph_text = next_p.get_text(strip=True)
                content.append({
                    "header": header_text,
                    "paragraph": paragraph_text
                })

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


def main():
    urls = load_urls("soussanahotel_links.json")
    print(f"📥 {len(urls)} URLs à scraper.\n")

    scraped_data = []
    for i, url in enumerate(urls, start=1):
        print(f"🔎 ({i}/{len(urls)}) Scraping : {url}")
        result = scrape_page(url)
        if result:
            scraped_data.append(result)
        time.sleep(1)  # Pour éviter de surcharger le site

    save_to_json(scraped_data)
    print("\n✅ Scraping terminé. Résultats enregistrés dans scraped_content.json")


# 🔹 Lancer le script
if __name__ == "__main__":
    main()
