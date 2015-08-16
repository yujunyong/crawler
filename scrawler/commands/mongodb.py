# -*- coding: utf-8 -*-

"""
    连接mongodb数据库，建立索引
"""

from pymongo import MongoClient

DATABASE_NAME = 'douban'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 27017
INDEX = {
    'book_info': {
        'isbn': {'name': 'isbn', 'unique': True}
    }
}

client = None

def drop_database(database):
    if database and client:
        client.drop_database(database)

def create_index():
    """
        创建索引
    """
    for collection, indexes in INDEX.items():
        for keys, kwargs in indexes.items():
            client[DATABASE_NAME][collection].create_index(keys, **kwargs)

if __name__ == '__main__':
    client = MongoClient(DATABASE_HOST, DATABASE_PORT)
    drop_database(DATABASE_NAME)
    create_index()
