# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuxjjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    sex  = scrapy.Field()
    user_sign = scrapy.Field()
    user_url = scrapy.Field()
    user_avatar = scrapy.Field()
    user_add = scrapy.Field()
    pass
