import json
import csv
import time
import requests
from bs4 import BeautifulSoup

# 1. Charger les URLs depuis le fichier JSON


def load_urls(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return [entry["url"] for entry in data]

# 2. Scraper une page HTML


def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Erreur HTTP {response.status_code} pour {url}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Titre
        title = soup.title.string.strip() if soup.title else "Sans titre"

        # Texte dans les balises h1, h2, p
        headers = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

        return {
            "url": url,
            "title": title,
            "headers": " | ".join(headers),
            "paragraphs": " | ".join(paragraphs)
        }

    except Exception as e:
        print(f"❌ Erreur lors du scraping de {url} : {e}")
        return None

# 3. Sauvegarder les résultats dans un CSV


def save_to_csv(data, filename="scraped_content.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["url", "title", "headers", "paragraphs"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            if row:
                writer.writerow(row)

# 4. Exécution principale


def main():
    urls = load_urls("soussanahotel_links.json")
    print(f"📥 {len(urls)} URLs à scraper.")

    scraped_data = []
    for i, url in enumerate(urls, start=1):
        print(f"🔎 ({i}/{len(urls)}) Scraping : {url}")
        result = scrape_page(url)
        if result:
            scraped_data.append(result)
        time.sleep(1)  # ⏱️ Pause pour éviter de surcharger le site

    save_to_csv(scraped_data)
    print("✅ Scraping terminé. Résultats enregistrés dans scraped_content.csv")


if __name__ == "__main__":
    main()
