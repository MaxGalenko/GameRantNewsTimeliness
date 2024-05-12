from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from AIAPIImplementation import *
from datetime import datetime
from dateutil import parser
from twitterText import *
import pytz


# uurl = "https://news.xbox.com/en-us/2024/05/06/xbox-military-appreciation-month-2024/"
# uurl = "https://news.xbox.com/en-us/2024/05/10/join-the-circuit-of-champions-event-now-through-may-23/"
# html = urlopen(url).read()
def parse_xbox_article(url):
    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
    soup = BeautifulSoup(response.content, features="html.parser")
    # print(soup)

    article_title = soup.find("h1")
    # if article_title is None:
    #     article_title = soup.find("h1", class_='xbox-legacy-header__title')
    # if article_title is None:
    #     print(url)
    article_title_text = article_title.get_text()
    # print(article_title_text)

    # Find the element with id "post__content"
    # article_body = soup.find("div", class_='post__content').find('div', class_='acf-innerblocks-container')
    print(url)
    article_body = soup.find("div", class_='post__content')
    if article_body is None:
        return None
    for aside in article_body(['aside']):
        aside.extract()
    summary_block = article_body.find('div', class_='wp-block-xbox-summary')
    if summary_block is not None:
        summary_block.extract()
    mspb_details = soup.find("div", class_='mspb-details')
    if mspb_details is not None:
        mspb_details.extract()

    article_body_text = article_body.get_text()

    # print(article_body_text)
    # timestamp = datetime.fromtimestamp(int(soup(['time'])[0]['datetime']), tz=pytz.utc)
    timestamp = soup.find('meta', {'property': 'article:published_time'})['content']
    timestamp = parser.parse(timestamp)
    keywords = get_keywords_array(article_body_text)

    return {
        'timestamp': timestamp,
        'publisher': 'XBox',
        'title': article_title_text,
        'keywords': keywords,
        'url': url
    }
    # print(soup(['time'])[0]['datetime'])
    # print(get_response_array(article_body_text))
    # print(article_title_text)
    # print(article_body_text)


def xbox_article_content(url):
        response = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
        soup = BeautifulSoup(response.content, features="html.parser")

        article_body = soup.find("div", class_='post__content')
        for aside in article_body(['aside']):
            aside.extract()
        summary_block = article_body.find('div', class_='wp-block-xbox-summary')
        if summary_block is not None:
            summary_block.extract()
        mspb_details = soup.find("div", class_='mspb-details')
        if mspb_details is not None:
            mspb_details.extract()

        article_body_text = article_body.get_text()

        return article_body_text

def xbox_tweet_content(url):
    content = get_xbox_tweets(url)
    return content