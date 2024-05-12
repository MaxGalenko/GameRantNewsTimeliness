import os
from dotenv import load_dotenv
from openai import OpenAI
import ast


class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Load environment variables
            load_dotenv()

            # Get API key
            api_key = os.getenv('API_KEY')

            cls._instance = super().__new__(cls)
            cls._instance.client = OpenAI(api_key=api_key)
        return cls._instance


# def load_openai_client():
#     # Load environment variables
#     load_dotenv()
#
#     # Get API key
#     api_key = os.getenv('API_KEY')
#
#     # Initialize OpenAI client
#     client = OpenAI(api_key=api_key)
#
#     return client


#
# load_dotenv()
#
# api_key = os.getenv('API_KEY')
#
# client = OpenAI(api_key=api_key)

# Gets response as python array
def get_keywords_array(plain_text_article):
    client = OpenAIClient().client
    # Generate response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": """You are a helpful assistant designed to output an array of minimum 10 to maximum 20 
             keywords from the article. I don't want the code markdown syntax. Instead of returning ```jsx[ 
             "keyword1",...]```, just give me ["keyword1",...]."""},
            {"role": "user", "content": plain_text_article}
        ]
    )


    print(response.choices[0].message.content)
    return ast.literal_eval(response.choices[0].message.content)


def matching_article_content(article1_content, article2_content):
    client = OpenAIClient().client
    user_prompt_content = article1_content + '\n===================\n' + article2_content
    # Generate response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": """You are a helpful assistant designed to compare news articles. You will be given 2 news articles, which will be seperated by a long string of '=' signs.
             You must check if the news are reporting on the same story. Return True if they're on the same story, and False if they aren't"""},
            {"role": "user", "content": user_prompt_content}
        ]
    )

    return response.choices[0].message.content

# response = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant designed to output JSON that contains the title of the article and an array of 10 keywords from the article."},
#     {"role": "user", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris auctor consectetur congue. Nulla eget turpis orci. Cras ac tortor quis ligula egestas volutpat a vitae massa. Aliquam nec accumsan est, id feugiat lacus. Nam ut magna nisl. Aenean iaculis hendrerit dui a semper. Sed placerat sem ante, sed congue nunc posuere id. Nunc viverra, magna a tempor lobortis, nulla magna vestibulum quam, a tristique nulla eros eu lacus. Fusce nec ultricies mi."}
#   ]
# )

# print(response.choices[0].message.content)
