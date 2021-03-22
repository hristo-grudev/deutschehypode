import scrapy

from scrapy.loader import ItemLoader

from ..items import DeutschehypodeItem
from itemloaders.processors import TakeFirst


class DeutschehypodeSpider(scrapy.Spider):
	name = 'deutschehypode'
	start_urls = ['https://www.deutsche-hypo.de/category/aktuelles-de']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="nächste"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space() and not(ancestor::div[@class="downloads-box hidden-print"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="entry-meta"]/text()').get()

		item = ItemLoader(item=DeutschehypodeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
