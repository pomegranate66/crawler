# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from json import dumps

'''写入文件中'''


class DoubanbookPipeline(object):
    def open_spider(self, spider):
        self.filename = open('books.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.filename.write(dumps(item, ensure_ascii=False))
        return item

    def close_spider(self, spider):
        self.filename.close()


import pymysql

'''mysql同步处理'''


class PyMySqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='crawl',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        insert_sql = "INSERT INTO book(name,star) VALUES ('%s','%s')" % (item['book_name'], item['book_star'])
        self.cursor.execute(insert_sql)
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


from twisted.enterprise import adbapi

'''mysql异步处理数据'''


class MySQLPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def _conditional_insert(self, tx, item):
        sql = "INSERT INTO book(name,star) VALUES ('%s','%s')" % (item['book_name'], item['book_star'])
        tx.execute(sql)

    def _handle_error(self, failue, item, spider):
        print(failue)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item


'''写入mongo数据库中'''
import pymongo


class MongoPipeline(object):
    def open_spider(self, spider):
        self.db = pymongo.MongoClient('mongodb://localhost:27017')
        self.collection = self.db.book

    def process_item(self, item, spider):
        self.collection.book.insert_one(dict(item))
        return item
