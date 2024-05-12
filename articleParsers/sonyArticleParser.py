from urllib.request import urlopen
from bs4 import BeautifulSoup

# url = "https://sonyinteractive.com/en/news/blog/marvels-spider-man-2-an-exclusive-look-into-the-brand-collaborations-surrounding-the-games-launch/"
url = "https://sonyinteractive.com/en/news/blog/inspiring-hope-sony-interactives-commitment-to-make-a-wish/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")
article_title = soup.find('h1', class_="post-title").get_text()

article_content = soup.find('div', class_='post-content')

for figureTag in article_content(["figure"]):
    figureTag.extract()

# get text
plain_text = article_content.get_text()

print(article_title)
print(plain_text)