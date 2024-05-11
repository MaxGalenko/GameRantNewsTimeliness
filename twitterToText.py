from ntscraper import Nitter

def check_tweets():
    # Initialize Nitter object
    nitter = Nitter()

    entry = 50
    start_date = '2024-01-20'
    end_date = '2024-04-15'

    # Getting the tweets
    xbox_tweets = nitter.get_tweets("Xbox", mode='user', number=entry)
    playstation_tweets = nitter.get_tweets("Playstation", mode='user', number=entry)

    # Printing the tweets
    def print_tweets(tweets_data, user):
        for tweet in tweets_data['tweets']:
            if tweet['user']['name'] == user:
                print(tweet['user']['name'])
                print(tweet['link'])
                print(tweet['text'])
                print(tweet['date'])
                print("-" * 50)

    print_tweets(xbox_tweets, "Xbox")
    print_tweets(playstation_tweets, "PlayStation")

# Call the function to start checking for new tweets from PlayStation
check_tweets()