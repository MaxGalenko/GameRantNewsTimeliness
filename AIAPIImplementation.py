import os
from dotenv import load_dotenv
from openai import OpenAI

def load_openai_client():
  # Load environment variables
  load_dotenv()

  # Get API key
  api_key = os.getenv('API_KEY')

  # Initialize OpenAI client
  client = OpenAI(api_key=api_key)

  return client

#
# load_dotenv()
#
# api_key = os.getenv('API_KEY')
#
# client = OpenAI(api_key=api_key)

# Gets response as python array
def get_response_array(client, plain_text_article):
  # Generate response
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system",
       "content": "You are a helpful assistant designed to output a python array that contains an array of 10 keywords from the article."},
      {"role": "user", "content": plain_text_article}
    ]
  )

  # Extract the array of keywords
  keyword_array = response.choices[0].message.content

  return keyword_array

# response = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant designed to output JSON that contains the title of the article and an array of 10 keywords from the article."},
#     {"role": "user", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris auctor consectetur congue. Nulla eget turpis orci. Cras ac tortor quis ligula egestas volutpat a vitae massa. Aliquam nec accumsan est, id feugiat lacus. Nam ut magna nisl. Aenean iaculis hendrerit dui a semper. Sed placerat sem ante, sed congue nunc posuere id. Nunc viverra, magna a tempor lobortis, nulla magna vestibulum quam, a tristique nulla eros eu lacus. Fusce nec ultricies mi."}
#   ]
# )

# client = load_openai_client()
# plain_text_article = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris auctor consectetur congue. Nulla eget turpis orci. Cras ac tortor quis ligula egestas volutpat a vitae massa. Aliquam nec accumsan est, id feugiat lacus. Nam ut magna nisl. Aenean iaculis hendrerit dui a semper. Sed placerat sem ante, sed congue nunc posuere id. Nunc viverra, magna a tempor lobortis, nulla magna vestibulum quam, a tristique nulla eros eu lacus. Fusce nec ultricies mi.'
# response = get_response_array(client, plain_text_article)
# print(response)

# print(response.choices[0].message.content)