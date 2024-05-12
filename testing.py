from database.databaseFunctions import *

article = {
    'timestamp': '2024-04-18T22:00:00+00:00',
    'publisher': 'GameRant',
    'title': 'article title here',
    'keywords': [
        'mario',
        'switch',
        'multiplayer'
    ],
    'url': 'https://ninentdo.com/article'
}

# print(insert_into_news_articles(article))
# print(cur.execute("""
# SELECT * FROM news_articles
# """))
retroactive_scan()