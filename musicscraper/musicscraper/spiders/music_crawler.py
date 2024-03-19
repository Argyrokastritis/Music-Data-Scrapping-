import scrapy
from ..items import MusicscraperItem

class MusicSpider(scrapy.Spider):
    name = 'music'
    start_urls = ['https://en.wikipedia.org/wiki/Music']

    def __init__(self, paragraph_name=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        self.paragraph_name = paragraph_name

    #TODO make the function parse better as it doesnt exactly parse what we want
    def parse(self, response):
        items = MusicscraperItem()

        # Select the section by its id
        section = response.xpath(f'//span[@id="{self.paragraph_name}"]/ancestor::h2/following-sibling::div[1]')

        # Extract the title, text, and urls within the section
        title = self.paragraph_name
        text = section.xpath('following-sibling::p[1]/text() | following-sibling::p[2]/text()').extract()
        urls = section.xpath('following-sibling::p[1]//a/@href | following-sibling::p[2]//a/@href').extract()

        items['title'] = title
        items['text'] = text
        items['urls'] = urls
        yield items
