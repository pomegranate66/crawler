# -*- coding: utf-8 -*-
import scrapy


class BingSpider(scrapy.Spider):
    name = 'bing'
    allowed_domains = ['bing.com']
    url = 'https://bing.ioliu.cn/'
    start_urls = [url]

    def parse(self, response):
        image_names = response.xpath('//div[@class="description"]/h3/text()').extract()
        image_urls = response.xpath('//div[@class="card progressive"]/img/@src').extract()
        next_url = response.xpath('//div[@class="page"]/a[2]/@href').extract_first()
        for n, u in zip(image_names, image_urls):
            yield {
                'image_name': n,
                'image_url': u
            }
        yield scrapy.Request(self.url+next_url,callback=self.parse)
