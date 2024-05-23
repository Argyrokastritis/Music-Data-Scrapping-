import scrapy
from ..items import MusicscraperItem
import sys


class MusicSpider(scrapy.Spider):
    name = 'music'

    start_urls = [
        'https://en.wikipedia.org/wiki/Music',
        'https://en.wikipedia.org/wiki/Musical_note',
        'https://en.wikipedia.org/wiki/Clef'
    ]

    def __init__(self, paragraph_name=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        self.paragraph_name = paragraph_name
        self.scraped_titles = set()

    # Define the URL to suffix mapping
    url_suffix_mapping = {
        'https://en.wikipedia.org/wiki/Music': 'of Music',
        'https://en.wikipedia.org/wiki/Musical_note': 'of Musical Note',
        'https://en.wikipedia.org/wiki/Clef': 'of Clef'
    }

    @classmethod
    def get_suffix(cls, url):
        for key in cls.url_suffix_mapping:
            if key in url:
                return cls.url_suffix_mapping[key]
        return ''

    def parse(self, response):
        items = MusicscraperItem()
        print("\n\n\n *********   The response is", response,  "********* \n\n\n")
        # Select the section by its id
        section = response.xpath(f'//span[@id="{self.paragraph_name}"]/ancestor::h2/following-sibling::div[1]')

        title = self.paragraph_name
        text = section.xpath('following-sibling::p[1]/text() | following-sibling::p[2]/text()').extract()
        urls = section.xpath('following-sibling::p[1]//a/@href | following-sibling::p[2]//a/@href').extract()

        # Get the suffix based on the URL
        suffix = self.get_suffix(response.url)
        title = f"{title} {suffix}"

        items['title'] = title
        items['text'] = text
        items['urls'] = urls

        # Print information with UTF-8 encoding
        self.print_utf8("The extracted title is: ", title)
        self.print_utf8("The data type of title is: ", type(title))

        self.print_utf8("The extracted text is: ", text)
        self.print_utf8("The data type of text is: ", type(text))
        for i, t in enumerate(text):
            self.print_utf8(f"The {i + 1}th element of the text list is: {t}")

        self.print_utf8("The extracted urls are: ", urls)
        self.print_utf8("The data type of urls is: ", type(urls))
        for i, u in enumerate(urls):
            self.print_utf8(f"The {i + 1}th element of the urls list is: {u}")

        yield items

    def print_utf8(self, *args):
        try:
            print(*[str(arg).encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding) for arg in args])
        except Exception as e:
            print(f"Error printing: {e}")
