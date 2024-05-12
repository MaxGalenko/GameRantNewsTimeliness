from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from articleParsers.ignArticleParser import *
import pytz


# def get_article_urls():
def get_article_urls(min_date, max_date):
    article_urls = []
    min_date = min_date.replace(tzinfo=pytz.utc)
    max_date = max_date.replace(tzinfo=pytz.utc)
    # Initialize WebDriver
    driver = webdriver.Chrome()  # You should replace this with the appropriate web driver you're using (Chrome, Firefox, etc.)

    # Open the URL of the webpage
    url = "https://www.ign.com/news"
    driver.get(url)

    # Automatically scroll the page
    scroll_pause_time = 2  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        oldest_article_link = soup.find_all('a', class_='item-body')[-1]
        oldest_article_url = 'https://www.ign.com' + oldest_article_link['href']
        oldest_timestamp = timestamp_ign_article(oldest_article_url)

        if oldest_timestamp < min_date:
            break

        # Check if reaching the end of the page
        # scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # if screen_height * i > scroll_height:
        #     break

    # Fetch the data using BeautifulSoup after all data is loaded
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for article in soup.find_all('a', class_='item-body'):
        article_url = 'https://www.ign.com' + article['href']
        article_timestamp = timestamp_ign_article(article_url)
        if article_timestamp > max_date or article_timestamp < min_date:
            continue
        article_urls.append(article_url)

    # Close the WebDriver session
    driver.quit()

    return article_urls

# min_date = datetime(year=2024, month=5, day=10, tzinfo=pytz.utc)
# max_date = datetime(year=2024, month=5, day=11, tzinfo=pytz.utc)

# print(get_article_urls(min_date, max_date))
