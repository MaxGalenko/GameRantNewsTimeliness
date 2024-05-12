from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://news.xbox.com/en-us/2024/05/06/xbox-military-appreciation-month-2024/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

article_title = soup.find(name="h1", class_="h2")

article_title_text = article_title.get_text()

print(article_title_text)

# Find the element with id "post__content"
article_body = soup.find(name="div", class_="wp-block-columns")

# Extract text only from the article body
if article_body:

    for figure_tag in article_body.find_all("figure"):
        figure_tag.extract()

    # Remove all div elements from the article body except those with class "content-block-regular"
    for div_tag in article_body.find_all("div"):
        if "content-block-regular" not in div_tag.get("class", []):
            div_tag.extract()

    # Get text from the article body
    article_text = article_body.get_text()

    # Split text into an array
    article_text_split = article_text.split()

    # Write text in one line
    cleaned_article_text = " ".join(article_text_split)

    print(cleaned_article_text)