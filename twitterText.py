import time
from AIAPIImplementation import get_keywords_array
from ntscraper import Nitter
from database.databaseFunctions import *

# Initialize Nitter object
nitter = Nitter()

entry = 50
start_date = '2024-01-20'
end_date = '2024-04-15'

data = []

# Getting the tweets
# Have to do this one by one and can't itirate in array because of rate limit issues
xbox_tweets = nitter.get_tweets("Xbox", mode='user', number=entry)
# playstation_tweets = nitter.get_tweets("Playstation", mode='user', number=entry)
# nintendo_tweets = nitter.get_tweets("NintendoAmerica", mode='user', number=entry)
epic_tweets = nitter.get_tweets("EpicGames", mode='user', number=entry)
# activision_tweets = nitter.get_tweets("Activision", mode='user', number=entry)
# ubisoft_tweets = nitter.get_tweets("Ubisoft", mode='user', number=entry)
# fortnite_tweets = nitter.get_tweets("FortniteGame", mode='user', number=entry)

def check_tweets():
    # Printing the tweets
    def add_tweets(tweets_data, user):
        for tweet in tweets_data['tweets']:
            if tweet['user']['name'] == user:
                plain_text_article = (tweet['text'])
                response = get_keywords_array(plain_text_article)
                datetime_obj = datetime.strptime(tweet['date'], "%b %d, %Y · %I:%M %p %Z")
                sample = {
                    'timestamp': datetime_obj,
                    'publisher': tweet['user']['name'],
                    'title': '',
                    'keywords': response,
                    'url': tweet['link']
                }
                if check_if_article_in_db(tweet['link']):
                    print('skipped')
                    continue
                insert_into_news_articles(sample)

                # sample_tuple = tuple(sample.items())
                # print(type(sample_tuple))
                # if sample_tuple not in data:
                #     data.add(sample_tuple)
    add_tweets(xbox_tweets, "Xbox")
    # add_tweets(playstation_tweets, "PlayStation")
    # add_tweets(nintendo_tweets, "NintendoAmerica")
    add_tweets(epic_tweets, "EpicGames")
    # add_tweets(ubisoft_tweets, "Ubisoft")
    # add_tweets(activision_tweets, "Activision")
    # add_tweets(fortnite_tweets, "FortniteGame")

    # for d in data:
    #     print(d)

def get_xbox_tweets(url):
    for tweet in xbox_tweets['tweets']:
        if tweet['link'] == url:
            return tweet['text']

def get_epic_tweets(url):
    for tweet in epic_tweets['tweets']:
        if tweet['link'] == url:
            return tweet['text']

# Call the function to start checking for new tweets from PlayStation
# check_tweets()
# while True:
#     check_tweets()
#     time.sleep(300)  # Sleep for 5 minutes