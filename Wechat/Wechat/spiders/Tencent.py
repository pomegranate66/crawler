# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'Tencent'

    def __init__(self, key=None, page=None, *args, **kwargs):
        super(TencentSpider, self).__init__(*args, **kwargs)
        self.url = 'https://weixin.sogou.com/weixin'
        self.page = page
        self.start_urls = ['https://weixin.sogou.com/weixin?query=%s&type=1' % key]

    def parse(self, response):
        tencent_name = response.xpath('//p[@class="tit"]').xpath('string(.)').extract()
        tencent_num = response.xpath('//p[@class="info"]').xpath('string(.)').extract()
        tencent_list = []
        tencent_info = response.xpath('//ul[@class="news-list2"]/li/dl[1]').xpath('string(.)').extract()
        next_url = response.xpath('//a[@id="sogou_next"]/@href').extract_first()
        for name, num in zip(tencent_name, tencent_num):
            print(name, num)
            tencent_list.append(name + ':' + num)
        for tencent, info in zip(tencent_list, tencent_info):
            yield {
                'tencent_list': tencent,
                'tencent_info': info
            }
        yield scrapy.Request(self.url + next_url, callback=self.parse)
