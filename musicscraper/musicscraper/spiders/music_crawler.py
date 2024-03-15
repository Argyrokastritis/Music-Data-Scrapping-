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
        title = section.xpath('.//h3/span[@class="mw-headline"]/text()').extract()
        text = section.xpath('.//p/text()').extract()
        urls = section.xpath('.//a/@href').extract()

        items['title'] = title
        items['text'] = text
        items['urls'] = urls
        yield items
