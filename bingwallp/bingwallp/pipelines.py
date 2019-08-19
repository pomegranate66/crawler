# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class BingwallpPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_url'], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = item['image_name'].replace(' ', '').replace('/', '&')
        return filename
