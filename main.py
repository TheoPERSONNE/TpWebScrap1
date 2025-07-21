# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def recuperer_article(url):
    entetes = {"User-Agent": "Mozilla/5.0"}
    reponse = requests.get(url, headers=entetes)
    reponse.encoding = reponse.apparent_encoding
    page = BeautifulSoup(reponse.text, "html.parser")

    titre_tag = page.find("h1", class_="entry-title")
    titre = titre_tag.text.strip() if titre_tag else "N/A"

    image_tag = page.find("img", class_="wp-post-image")
    miniature = urljoin(url, image_tag["src"]) if image_tag and image_tag.get("src") else "N/A"

    sous_categorie = "N/A"
    post_in = page.find("span", class_="posted-in")
    if post_in:
        liens = post_in.find_all("a")
        if liens:
            sous_categorie = liens[-1].text.strip()

    resume = "N/A"
    resume_div = page.find("div", class_="entry-summary")
    if resume_div:
        resume = resume_div.text.strip()
    else:
        premier_p = page.find("div", class_="entry-content").find("p")
        if premier_p:
            resume = premier_p.text.strip()

    date_publication = "N/A"
    date_span = page.find("span", class_="posted-on")
    if date_span:
        time_tag = date_span.find("time")
        if time_tag and time_tag.has_attr("datetime"):
            date_publication = time_tag["datetime"][:10]

    auteur = "N/A"
    auteur_span = page.find("span", class_="author vcard")
    if auteur_span:
        auteur = auteur_span.text.strip()

    contenu_texte = ""
    contenu_div = page.find("div", class_="entry-content")
    if contenu_div:
        for balise in contenu_div(["script", "style"]):
            balise.decompose()
        contenu_texte = "\n\n".join(p.get_text(strip=True) for p in contenu_div.find_all("p"))

    images = []
    if contenu_div:
        for image in contenu_div.find_all("img"):
            url_image = urljoin(url, image.get("src", ""))
            legende = image.get("alt") or image.get("title") or ""
            images.append({"url": url_image, "legende": legende})

    article = {
        "url": url,
        "titre": titre,
        "miniature": miniature,
        "sous_categorie": sous_categorie,
        "resume": resume,
        "date_publication": date_publication,
        "auteur": auteur,
        "contenu": contenu_texte,
        "images": images,
    }
    return article

def afficher_article(article):
    print("\n=== ARTICLE ===")
    print(f"Titre : {article['titre']}")
    print(f"URL Miniature : {article['miniature']}")
    print(f"Sous-categorie : {article['sous_categorie']}")
    print(f"Resume : {article['resume']}")
    print(f"Date de publication : {article['date_publication']}")
    print(f"Auteur : {article['auteur']}")
    print("\nContenu :\n", article['contenu'])
    print("\nImages dans l'article :")
    for i, img in enumerate(article['images'], 1):
        print(f"  {i}. URL : {img['url']}")
        print(f"     Legende : {img['legende']}")
    print("=====================\n")


if __name__ == "__main__":
    url_test = "https://www.blogdumoderateur.com/openai-presente-agent-chatgpt-prendre-controle-pc/"
    article = recuperer_article(url_test)
    afficher_article(article)
