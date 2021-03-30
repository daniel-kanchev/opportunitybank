import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from opportunitybank.items import Article


class opportunitybankSpider(scrapy.Spider):
    name = 'opportunitybank'
    start_urls = ['https://www.opportunitybank.com/blog']

    def parse(self, response):
        links = response.xpath('//p/a[@class="Button1"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//td/h2/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//table[@class="Subsection-Table"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
