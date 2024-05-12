from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from AIAPIImplementation import *
from datetime import datetime
from dateutil import parser
import pytz


def parse_ign_article(url):
    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
    soup = BeautifulSoup(response.content, features="html.parser")
    # print(soup)

    article_title = soup.find("h1")

    article_title_text = article_title.get_text()
    article_body = soup.find("section", class_='article-page')
    if article_body is None:
        article_body = soup.find('div', {'itemprop': 'description'})
    if article_body is None:
        return None
    for div in article_body(['div']):
        div.extract()
    for output in article_body(['output']):
        output.extract()

    article_body_text = article_body.get_text()

    # print(article_body_text)
    # timestamp = datetime.fromtimestamp(int(soup(['time'])[0]['datetime']), tz=pytz.utc)
    timestamp = soup.find('meta', {'property': 'article:published_time'})['content']
    timestamp = parser.parse(timestamp)
    keywords = get_keywords_array(article_body_text)

    return {
        'timestamp': timestamp,
        'publisher': 'IGN',
        'title': article_title_text,
        'keywords': keywords,
        'url': url
    }

def timestamp_ign_article(url):
    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
    soup = BeautifulSoup(response.content, features="html.parser")
    # print(soup)

    timestamp = soup.find('meta', {'property': 'article:published_time'})['content']
    timestamp = parser.parse(timestamp)

    return timestamp

def ign_article_content(url):
    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
    soup = BeautifulSoup(response.content, features="html.parser")
    # print(soup)

    article_title = soup.find("h1")

    article_title_text = article_title.get_text()
    article_body = soup.find("section", class_='article-page')
    if article_body is None:
        article_body = soup.find('div', {'itemprop': 'description'})
    if article_body is None:
        return None
    for div in article_body(['div']):
        div.extract()
    for output in article_body(['output']):
        output.extract()

    article_body_text = article_body.get_text()

    return article_body_text
