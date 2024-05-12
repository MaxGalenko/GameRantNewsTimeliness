from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://sonyinteractive.com/en/news/blog/marvels-spider-man-2-an-exclusive-look-into-the-brand-collaborations-surrounding-the-games-launch/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

article_title = soup.find(name="h1", class_="post-title")

article_title_text = article_title.get_text()

print(article_title_text)

# Find div element with id "post-content"
article_body = soup.find(name="div", class_="post-content")

# Extract text only from the article body
if article_body:

    for figureTag in article_body(["figure"]):
        figureTag.extract()

    # Get text from the article body
    article_text = article_body.get_text()

    # Split text into an array
    article_text_split = article_text.split()

    # Write text in one line
    cleaned_article_text = " ".join(article_text_split)

    print(cleaned_article_text)