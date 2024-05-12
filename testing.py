from database.databaseFunctions import *
from scanPublisherByDateRange.xboxScanner import *
# from articleParsers.XboxArticleParser import *
from scanPubs import *
import importlib

# write_gamerant_excel_to_database()

date_range = get_gamerant_date_range()

publishers = ['xbox']

for publisher in publishers:
    scanner = importlib.import_module(f'scanPublisherByDateRange.{publisher}Scanner')
    get_article_urls = getattr(scanner, 'get_article_urls')
    article_urls = get_article_urls(date_range['min_date'], date_range['max_date'])

    parser = importlib.import_module(f'articleParsers.{publisher}ArticleParser')
    parse_article = getattr(parser, f'parse_{publisher}_article')
    for article_url in article_urls:
        if check_if_article_in_db(article_url):
            print('skipped')
            continue
        article_obj = parse_article(article_url)
        if article_obj is None:
            continue
        insert_into_news_articles(article_obj)

retroactive_scan()

