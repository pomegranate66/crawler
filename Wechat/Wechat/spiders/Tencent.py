# -*- coding: utf-8 -*-
import scrapy

from Wechat.items import WechatItem


class TencentSpider(scrapy.Spider):
    name = 'Tencent'

    def __init__(self, key=None, page=None, *args, **kwargs):
        super(TencentSpider, self).__init__(*args, **kwargs)
        self.url = 'https://weixin.sogou.com/weixin'
        self.page = page
        self.start_urls = ['https://weixin.sogou.com/weixin?query=%s&type=1' % key]

    def parse(self, response):
        tencent_names = response.xpath('//p[@class="tit"]').xpath('string(.)').extract()
        tencent_nums = response.xpath('//p[@class="info"]').xpath('string(.)').extract()
        tencent_infos = response.xpath('//ul[@class="news-list2"]/li/dl[1]').xpath('string(.)').extract()
        next_url = response.xpath('//a[@id="sogou_next"]/@href').extract_first()

        for name, number, info in zip(tencent_names, tencent_nums, tencent_infos):
            yield {
                'tencent_name':name,
                'tencent_number':number,
                'tencent_info':info,
            }

        # yield scrapy.Request(self.url + next_url, callback=self.parse)
