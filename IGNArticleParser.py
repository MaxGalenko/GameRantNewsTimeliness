from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.ign.com/articles/microsoft-closes-redfall-developer-arkane-austin-hifi-rush-developer-tango-gameworks-and-more-in-devastating-cuts-at-bethesda/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

article_title = soup.find(name="h1", class_="display-title jsx-2885892373")

article_title_text = article_title.get_text()

print(article_title_text)

# Find section element with id "article-body"
article_body = soup.find(name="section", class_="article-page")

# Extract text only from the article body
if article_body:

    # Remove all div elements from the article body except those with class "content-block-regular"
    for iframe_tag in article_body.find_all("iframe"):
        iframe_tag.extract()

    # Get text from the article body
    article_text = article_body.get_text()

    # Split text into an array
    article_text_split = article_text.split()

    # Write text in one line
    cleaned_article_text = " ".join(article_text_split)

    print(cleaned_article_text)