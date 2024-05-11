import os, WebToPlainText
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('API_KEY')

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON that contains the title of the article and an array of 10 keywords from the article."},
    {"role": "user", "content": WebToPlainText.cleaned_plain_text}
  ]
)

print(response.choices[0].message.content)