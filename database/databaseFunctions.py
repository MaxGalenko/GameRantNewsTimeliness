import psycopg2
from datetime import datetime
import pandas as pd
import atexit
import importlib

import sys

sys.path.append("..")
from AIAPIImplementation import *


@atexit.register
def close_connection_pool():
    conn.commit()
    conn.close()


conn = psycopg2.connect(database="gamerantb1",
                        user="postgres",
                        host='localhost',
                        password="gamerantb1",
                        port=5432)

cur = conn.cursor()


def create_tables():
    print('create tables')


def ask_gpt_if_related(gamerant_article_content, outside_article):
    outside_publisher = outside_article[2]
    outside_url = outside_article[5]
    outside_title = outside_article[3]

    parser = importlib.import_module(f'articleParsers.{(outside_publisher.lower())}ArticleParser')
    if outside_title is not None:
        article_content_getter = getattr(parser, f'{outside_publisher.lower()}_article_content')
    else:
        article_content_getter = getattr(parser, f'{outside_publisher.lower()}_tweet_content')

    outside_article_content = article_content_getter(outside_url)

    matching_article_content(gamerant_article_content, outside_article_content)

    return True


def match_news_case(article):
    # select current news cases with matching keywords
    cur.execute("""
        SELECT news_cases.*, news_articles.url FROM news_cases
        INNER JOIN news_articles
        ON news_cases.first_article_id = news_articles.article_id
        WHERE news_cases.status='current_news'
        AND (
        SELECT COUNT(DISTINCT unnest(%(keywords)s) INTERSECT SELECT DISTINCT unnest(news_cases.keywords))
        ) >= 5
        AND news_cases.gamerant_article_id != null
        """, article)

    # if select isn't empty, compare content with chatgpt
    if cur.rowcount > 0:
        keywords_matched_news_cases = cur.fetchall()
        for row in keywords_matched_news_cases:
            url1 = article['url']
            url2 = row[5]
            if ask_gpt_if_related(url1, url2):
                return True, row[0]

    # either keywords select was empty, or chatgpt didn't say articles were related
    return False, 0


def check_if_article_in_db(article_url):
    cur.execute("""
    SELECT * FROM news_articles
    WHERE url=%(url)s""", {'url': article_url})
    return cur.rowcount > 0


def insert_into_news_articles(article):
    print(article['keywords'])
    cur.execute("""
        INSERT INTO news_articles(timestamp, publisher, title, keywords, url)
        VALUES(%(timestamp)s, %(publisher)s, %(title)s, %(keywords)s, %(url)s)
        RETURNING article_id
        """,
                article)

    new_article_id = cur.fetchone()[0]
    return new_article_id


def new_outside_article(article):
    new_article_id = insert_into_news_articles(article)
    # cur.execute("""
    # SELECT * FROM news_cases WHERE status='current_news' AND
    # (
    # SELECT COUNT(DISTINCT unnest(%(keywords)s) INTERSECT SELECT DISTINCT unnest(keywords))
    # ) >= 3
    # """, article)
    #
    #
    # if cur.rowcount == 0:
    # first article on the topic, create new row
    if not match_news_case(article)[0]:
        cur.execute("""
            INSERT INTO news_cases(first_article_id, gamerant_article_id, keywords, status)
            VALUES(%(first_article_id)s, %(keywords)s, null, 'current_news')
            """,
                    {'keywords': article['keywords'], 'first_article_id': new_article_id})


def new_gamerant_article(article):
    new_article_id = insert_into_news_articles(article)

    matched, case_id = match_news_case(article)
    if matched:
        cur.execute("""
        UPDATE news_cases
        SET gamerant_article_id=%(gamerant_article_id)s
        WHERE case_id=%(case_id)s
        """,
                    {'gamerant_article_id': new_article_id, 'case_id': case_id})


"""
article =
{
    'timestamp': '2024-04-18T20:00:00+00:00',
    'publisher': 'Nintendo',
    'title': 'article title here',
    'keywords': [
        'mario',
        'switch',
        'multiplayer'
    ],
    'url': 'https://ninentdo.com/article' 
}
"""


def new_article(article):
    # article['timestamp'] = datetime.now()

    if article['publisher'] == 'GameRant':
        new_gamerant_article(article)
    else:
        new_outside_article(article)


def retroactive_scan():
    # select all gamerant articles
    cur.execute("""
    SELECT * FROM news_articles
    WHERE publisher='GameRant'
    """)

    first_iter = True
    gamerant_articles = cur.fetchall()
    for gamerant_article in gamerant_articles:
        gamerant_url = gamerant_article[5]
        gamerant_title = gamerant_article[3]
        gamerant_timestamp = gamerant_article[1]

        parser = importlib.import_module('articleParsers.GameRantArticleParser')
        article_content_getter = getattr(parser, 'gamerant_article_content')
        gamerant_article_content = article_content_getter(gamerant_url)

        first_pub_url = None
        first_pub_timestamp = None

        cur.execute("""
                SELECT * FROM news_articles
                WHERE publisher!='GameRant'
                AND (
                SELECT COUNT(*)
                FROM unnest(keywords) AS keyword
                WHERE keyword = ANY(%(keywords)s)
                ) >= 5
                """,
                    {'keywords': gamerant_article[4]})

        # if select isn't empty, compare content with chatgpt
        if cur.rowcount > 0:
            keywords_matched_news_cases = cur.fetchall()
            for row in keywords_matched_news_cases:
                url1 = gamerant_url
                url2 = row[5]
                article_timestamp = row[1]
                # if articles are related and outside article's release date is the oldest one found so far
                if ask_gpt_if_related(gamerant_article_content, row) and (
                        first_pub_timestamp is None or article_timestamp < first_pub_timestamp):
                    first_pub_url = url2
                    first_pub_timestamp = article_timestamp

        delta_time = gamerant_timestamp
        if first_pub_timestamp is not None:
            delta_time -= first_pub_timestamp

        df = pd.DataFrame(data={'GameRant URL': [gamerant_url], 'GameRant Title': gamerant_title,
                                'GameRant Timestamp': gamerant_timestamp, 'First Announcement Url': first_pub_url,
                                'First Announcement Timestamp': first_pub_timestamp, 'Delta Time': delta_time})
        df.to_csv('output.csv', mode='a', header=first_iter)
        first_iter = False


def get_gamerant_date_range():
    cur.execute("""
            SELECT MIN(timestamp) 
            FROM news_articles
            WHERE publisher = 'GameRant'
            """,
                )
    conn.commit()
    min_date = cur.fetchone()[0]

    cur.execute("""
                SELECT MAX(timestamp) 
                FROM news_articles
                WHERE publisher = 'GameRant'
                """,
                )
    conn.commit()
    max_date = cur.fetchone()[0]

    date_range = {
        "min_date": min_date,
        "max_date": max_date
    }
    return date_range
