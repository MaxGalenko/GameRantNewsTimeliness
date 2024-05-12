from AIAPIImplementation import load_openai_client, get_response_array
from ntscraper import Nitter

def check_tweets():
    # Initialize Nitter object
    nitter = Nitter()

    entry = 2
    start_date = '2024-01-20'
    end_date = '2024-04-15'

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
    def print_tweets(tweets_data, user):
        for tweet in tweets_data['tweets']:
            if tweet['user']['name'] == user:
                print(tweet['user']['name'])
                print(tweet['link'])
                plain_text_article = (tweet['text'])
                response = get_response_array(client, plain_text_article)
                print(response)
                print(tweet['date'])
                print("-" * 50)

    print_tweets(xbox_tweets, "Xbox")
    print_tweets(playstation_tweets, "PlayStation")
    # print_tweets(nintendo_tweets, "NintendoAmerica")
    # print_tweets(epic_tweets, "EpicGames")
    # print_tweets(ubisoft_tweets, "Ubisoft")
    # print_tweets(activision_tweets, "Activision")
    # print_tweets(fortnite_tweets, "FortniteGame")

# Call the function to start checking for new tweets from PlayStation
check_tweets()