# -*- coding: utf-8 -*-
import scrapy
from time import sleep

class DoubanSpider(scrapy.Spider):
    name = 'DouBan'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/top250?start=0']

    def parse(self, response):
        sleep(3)
        book_stars = response.xpath('//span[@class="rating_nums"]').xpath('string(.)').extract()
        book_names = []
        for name in response.xpath('//div[@class="pl2"]/a').xpath('string(.)').extract():
            book_names.append(name.replace('\n','').replace(' ',''))
        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        for n,s in zip(book_names,book_stars):
            yield {
                'book_name':n,
                'book_star':s
            }
        yield scrapy.Request(next_url,callback=self.parse)