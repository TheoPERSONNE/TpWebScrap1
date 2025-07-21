import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extraire_articles(html):
    soup = BeautifulSoup(html, "html.parser")
    articles_html = soup.select("article.post")
    liste_articles = []

    for article_html in articles_html:
        # Titre
        titre_tag = article_html.select_one("h3.entry-title")
        titre = titre_tag.get_text(strip=True) if titre_tag else "Sans titre"

        # Image miniature principale
        img_tag = article_html.select_one(".post-thumbnail img")
        if img_tag:
            url_image_mini = img_tag.get("data-lazy-src") or img_tag.get("src")
            alt_image = img_tag.get("alt") or ""
        else:
            url_image_mini, alt_image = None, ""

        # Sous-categorie (sans accent ici)
        sous_categorie_tag = article_html.select_one("span.favtag")
        sous_categorie = sous_categorie_tag.get_text(strip=True) if sous_categorie_tag else "Sans sous-categorie"

        # Resume
        resume_tag = article_html.select_one("div.entry-excerpt")
        resume = resume_tag.get_text(strip=True) if resume_tag else ""

        # Date publication AAAA-MM-JJ
        date_tag = article_html.select_one("time.entry-date")
        date_pub = None
        if date_tag and date_tag.has_attr("datetime"):
            try:
                date_pub = datetime.fromisoformat(date_tag["datetime"]).date().isoformat()
            except ValueError:
                date_pub = "Date invalide"
        else:
            date_pub = "Date non trouvee"

        # Auteur (pas dispo ici)
        auteur = "Auteur non specifie"

        # Contenu (ici on prend juste le resume)
        contenu = resume

        # Images dans l’article (vide ici)
        images_article = []

        article = {
            "titre": titre,
            "image_miniature": {
                "url": url_image_mini,
                "alt": alt_image
            },
            "sous_categorie": sous_categorie,
            "resume": resume,
            "date_publication": date_pub,
            "auteur": auteur,
            "contenu": contenu,
            "images": images_article
        }
        liste_articles.append(article)

    return liste_articles

if __name__ == "__main__":
    url = "https://www.blogdumoderateur.com"
    reponse = requests.get(url)
    reponse.encoding = 'utf-8'

    articles = extraire_articles(reponse.text)

    for i, art in enumerate(articles, 1):
        print(f"\n=== Article #{i} ===")
        print(f"Titre           : {art['titre']}")
        print(f"Image miniature : {art['image_miniature']['url']}")
        print(f"  Description   : {art['image_miniature']['alt']}")
        print(f"Sous-categorie  : {art['sous_categorie']}")
        print(f"Resume          : {art['resume']}")
        print(f"Date publication: {art['date_publication']}")
        print(f"Auteur          : {art['auteur']}")
        print(f"Contenu         : {art['contenu'][:100]}...")
        print(f"Images article  : {len(art['images'])} images\n")
