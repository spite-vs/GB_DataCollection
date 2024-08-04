# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashImageItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
