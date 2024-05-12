from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

def get_article_urls(min_date, max_date):
    for single_date in (min_date + timedelta(n) for n in range(max_date - min_date)):
        year = single_date.year
        month = single_date.month
        day = single_date.day

        response = requests.get(f'https://news.xbox.com/en-us/{year}/{month}/{day}/')
        soup = BeautifulSoup(response.content, features="html.parser")

