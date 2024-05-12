from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def get_article_urls(min_date, max_date):
    article_urls = []
    for single_date in (min_date + timedelta(n) for n in range((max_date - min_date).days)):
        year = single_date.year
        month = single_date.month
        day = single_date.day

        response = requests.get(f'https://news.xbox.com/en-us/{year}/{month}/{day}/',
                                headers={
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                                                  'KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                                              'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
        soup = BeautifulSoup(response.content, features="html.parser")
        for article in soup(['article']):
            url = article.find('a', class_='featured-image')['href']
            if 'news.xbox' not in url:
                continue
            article_urls.append(url)

    return article_urls


# min_date = datetime(year=2024, month=5, day=1)
# max_date = datetime(year=2024, month=6, day=1)
#
# get_article_urls(min_date, max_date)
