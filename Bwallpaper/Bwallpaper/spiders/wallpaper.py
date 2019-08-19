# -*- coding: utf-8 -*-
import scrapy
# from Bwallpaper.Bwallpaper.input_url import Application

class WallpaperSpider(scrapy.Spider):
    name = 'wallpaper'
    allowed_domains = ['desk.zol.com.cn']
    url = 'http://desk.zol.com.cn'
    x = input('请输入你要爬取的壁纸的第一页网址:(最后加一个空格)')
    start_urls = [x[0]]

    def parse(self, response):
        image_name = response.xpath('/html/body/div[3]/h3')[0].xpath('string(.)').extract_first().replace('\r\n\t\t',
                                                                                                          '').strip()
        image_url = response.xpath('//img[@id="bigImg"]/@src').extract_first()
        next_url = response.xpath('//a[@id="pageNext"]/@href').extract_first()
        yield {
            'image_name': image_name,
            'image_url': image_url,
        }
        yield scrapy.Request(self.url + next_url, callback=self.parse)
