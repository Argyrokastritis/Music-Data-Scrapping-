import scrapy
from ..items import MusicscraperItem


class MusicSpider(scrapy.Spider):
    name = 'music'

    #TODO add more urls to extract data from
    start_urls = ['https://en.wikipedia.org/wiki/Music']

    def __init__(self, paragraph_name=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        self.paragraph_name = paragraph_name

    #TODO make the function parse better as it doesnt exactly parse what we want
    def parse(self, response):
        items = MusicscraperItem()

        # Select the section by its id
        section = response.xpath(f'//span[@id="{self.paragraph_name}"]/ancestor::h2/following-sibling::div[1]')

        title = self.paragraph_name
        text = section.xpath('following-sibling::p[1]/text() | following-sibling::p[2]/text()').extract()
        urls = section.xpath('following-sibling::p[1]//a/@href | following-sibling::p[2]//a/@href').extract()

        items['title'] = title
        items['text'] = text
        items['urls'] = urls

        print("The extracted title is: ", title)
        print("The data type of title is: ", type(title))

        print("The extracted text is: ", text)
        print("The data type of text is: ", type(text))
        for i, t in enumerate(text):
            print(f"The {i + 1}th element of the text list is: {t}")

        print("The extracted urls are: ", urls)
        print("The data type of urls is: ", type(urls))
        for i, u in enumerate(urls):
            print(f"The {i + 1}th element of the urls list is: {u}")

        yield items
