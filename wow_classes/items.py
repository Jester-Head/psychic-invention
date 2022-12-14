# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WowClassesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment = scrapy.Field()
    date = scrapy.Field()
    post_count = scrapy.Field()
    likes = scrapy.Field()
    ids = scrapy.Field()
    topic= scrapy.Field()
    pass
