# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from json import dumps


class WechatPipeline(object):
    def open_spider(self, spider):
        self.filename = open('tencent.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        item['tencent_list'] = item['tencent_list'].replace('\n', '')
        item['tencent_info'] = item['tencent_info'].replace('\n', '')
        self.filename.write(dumps(item, ensure_ascii=False) + '\n')
        return item

    def close_spider(self, spider):
        self.filename.close()
