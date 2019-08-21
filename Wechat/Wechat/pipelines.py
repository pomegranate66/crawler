# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from json import dumps
import pymysql
from twisted.enterprise import adbapi


class WechatPipeline(object):
    def open_spider(self, spider):
        self.filename = open('tencent.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.filename.write(dumps(item,ensure_ascii=False) + '\n')
        return item

    def close_spider(self, spider):
        self.filename.close()


class WechatMySQLPipeline(object):

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
        sql = "INSERT INTO wechat(name,number,content) VALUES ('%s','%s','%s')" % (item['tencent_name'], item['tencent_number'],item['tencent_info'])
        tx.execute(sql)

    def _handle_error(self, failue, item, spider):
        print(failue)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item
