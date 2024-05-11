import scrapy
from scrapy.crawler import CrawlerProcess
import lxml.html

# Create a spider
class ExampleSpider(scrapy.Spider):
    name = 'example'
    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'LOG_LEVEL': 'CRITICAL',  # Only log critical errors
        'LOG_FILE': 'log.txt',  # Save log to file
    }

    # Define a list of start URLs
    start_urls = [
        "https://gamerant.com/palworld-peta-statement/"
    ]

    def parse(self, response):
        # Parse the response
        content = lxml.html.fromstring(response.body)

        # Strip unwanted elements like <script> and <head>
        lxml.etree.strip_elements(content, lxml.etree.Comment, "script", "head")

        # complete text
        plain_text = lxml.html.tostring(content, method="text", encoding="unicode")

        # split text into an array to get rid of the useless spaces, tabs and whitespaces
        plain_text_split = plain_text.split()

        # write text into one line separated by spaces
        cleaned_plain_text = " ".join(plain_text_split)

        print(cleaned_plain_text)

process = CrawlerProcess()
process.crawl(ExampleSpider)
process.start()