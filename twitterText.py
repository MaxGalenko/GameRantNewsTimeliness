import time
from AIAPIImplementation import load_openai_client, get_response_array
from ntscraper import Nitter

def check_tweets():
    # Initialize Nitter object
    nitter = Nitter()

    entry = 2
    start_date = '2024-01-20'
    end_date = '2024-04-15'

    data = set()

    # Getting the tweets
    # Have to do this one by one and can't itirate in array because of rate limit issues
    xbox_tweets = nitter.get_tweets("Xbox", mode='user', number=entry)
    playstation_tweets = nitter.get_tweets("Playstation", mode='user', number=entry)
    # nintendo_tweets = nitter.get_tweets("NintendoAmerica", mode='user', number=entry)
    # epic_tweets = nitter.get_tweets("EpicGames", mode='user', number=entry)
    # activision_tweets = nitter.get_tweets("Activision", mode='user', number=entry)
    # ubisoft_tweets = nitter.get_tweets("Ubisoft", mode='user', number=entry)
    # fortnite_tweets = nitter.get_tweets("FortniteGame", mode='user', number=entry)

    client = load_openai_client()

    # Printing the tweets
    def add_tweets(tweets_data, user):
        nonlocal data
        for tweet in tweets_data['tweets']:
            if tweet['user']['name'] == user:
                plain_text_article = (tweet['text'])
                response = get_response_array(client, plain_text_article)
                sample = {
                    'timestamp': tweet['date'],
                    'publisher': tweet['user']['name'],
                    'title': '',
                    'keywords': response,
                    'url': tweet['link']
                }
                sample_tuple = tuple(sample.items())
                if sample_tuple not in data:
                    data.add(sample_tuple)

    add_tweets(xbox_tweets, "Xbox")
    add_tweets(playstation_tweets, "PlayStation")
    # add_tweets(nintendo_tweets, "NintendoAmerica")
    # add_tweets(epic_tweets, "EpicGames")
    # add_tweets(ubisoft_tweets, "Ubisoft")
    # add_tweets(activision_tweets, "Activision")
    # add_tweets(fortnite_tweets, "FortniteGame")

    for d in data:
        print(d)

# Call the function to start checking for new tweets from PlayStation
while True:
    check_tweets()
    time.sleep(300)  # Sleep for 5 minutes