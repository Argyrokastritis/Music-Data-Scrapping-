import scrapy
from ..items import MusicscraperItem



class MusicSpider(scrapy.Spider):
    name = 'music'
    start_urls = [
        'https://en.wikipedia.org/wiki/Music'

    ]

    def parse(self, response):
        items = MusicscraperItem()

        title = response.css('.mw-page-title-main::text').extract()
        text = response.css('p::text').extract()
        urls = response.css('a::text').extract()

        items['title'] = title
        items['text'] = text
        items['urls'] = urls
        yield items
