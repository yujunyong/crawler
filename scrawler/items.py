# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class BookInfoItem(Item):
    evaluate = Field()
    author = Field()
    publisher = Field()
    publish_year = Field()
    page = Field()
    price = Field()
    isbn = Field()
    content_desc = Field()
    author_desc = Field()
    douban_url = Field()

