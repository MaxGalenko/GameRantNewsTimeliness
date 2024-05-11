from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://gamerant.com/epic-games-store-free-games-march-2024-deus-ex-bridge-egs/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# Find the element with id "article-body"
article_body = soup.find(id="article-body")

# Extract text only from the article body
if article_body:
    # Remove script and style elements from the article body
    for script in article_body(["script", "style"]):
        script.extract()    # rip it out

    # Remove all div elements from the article body except those with class "content-block-regular"
    for div in article_body.find_all("div"):
        if "content-block-regular" not in div.get("class", []):
            div.extract()

    # Get text from the article body
    article_text = article_body.get_text()

    # Split text into an array
    article_text_split = article_text.split()

    # Write text in one line
    cleaned_article_text = " ".join(article_text_split)

    print(cleaned_article_text)
else:
    print("Could not find article body with id 'article-body'")