# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanBookItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field()
    date = scrapy.Field()
    page = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    ISBN = scrapy.Field()
    author_profile = scrapy.Field()
    content_description = scrapy.Field()
    link = scrapy.Field()
    pass