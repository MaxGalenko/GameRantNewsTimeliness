from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://gamerant.com/epic-games-store-free-games-march-2024-deus-ex-bridge-egs/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
plain_text = soup.get_text()

# split text into an array
plain_text_split = plain_text.split()

# write text in one line
cleaned_plain_text = " ".join(plain_text_split)