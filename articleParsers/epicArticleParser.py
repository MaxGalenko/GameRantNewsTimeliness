from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from AIAPIImplementation import *
from datetime import datetime
from dateutil import parser
from twitterText import *
import pytz

def parse_epic_article(url):
    return {
    }

def epic_article_content(url):
        article_body_text=''
        return article_body_text

def epic_tweet_content(url):
    content = get_epic_tweets(url)
    return content