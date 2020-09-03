# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem


class NewsItem(DjangoItem):
    titulo = scrapy.Field()
    link = scrapy.Field()
    site = scrapy.Field()
    data = scrapy.Field()