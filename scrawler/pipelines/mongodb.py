# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class MongoPipeLine(object):
    collection_name = 'book_info'

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('DATABASE_HOST', 'localhost'),
            mongo_port=crawler.settings.get('DATABASE_PORT', 27017),
            mongo_db=crawler.settings.get('DATABASE_NAME')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 如果还没有相同isbn的数据，则插入数据
        if self.db[self.collection_name].find({'isbn': item['isbn']}).count() == 0:
            self.db[self.collection_name].insert(dict(item))
        else:
            spider.logger.debug('already has isbn %s, do not insert data', item['isbn'])

        return item
