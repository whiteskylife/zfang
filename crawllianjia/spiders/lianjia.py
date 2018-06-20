# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from crawllianjia.items import lianjiaItem
from http import cookiejar
import scrapy_redis

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']

    def start_requests(self):
        page = 1
        url = 'https://sz.lianjia.com/ershoufang/pg%s/' % page
        yield Request(url=url, callback=self.parse_index)


    def parse_index(self, response):
        content_urls = response.xpath(
            '//div[contains(@class,"content")]//ul[contains(@class,"sellListContent")]//li/a[1]/@href').extract()
        for url in content_urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        item = lianjiaItem()
        item['url'] = response.url
        item['price'] = ''.join(response.xpath(
            '//div[@class="overview"]//div[contains(@class, "price")]/span[position()<3]//text()').extract())
        item['unitPrice'] = ''.join(
            response.xpath('//div[@class="overview"]//div[contains(@class, "unitPrice")]//span//text()').extract())
        item['room'] = ''.join(
            response.xpath('//div[@class="overview"]//div[contains(@class, "room")]//div//text()').extract())
        item['type'] = ' '.join(
            response.xpath('//div[@class="overview"]//div[contains(@class, "type")]//div//text()').extract())
        item['area'] = ' '.join(
            response.xpath('//div[@class="overview"]//div[contains(@class, "area")]//div//text()').extract())
        item['communityName'] = response.xpath(
            '//div[@class="overview"]//div[contains(@class, "communityName")]//a[1]/text()').extract_first()
        item['areaName'] = ' '.join(
            response.xpath('//div[@class="overview"]//div[contains(@class, "areaName")]//a/text()').extract())
        item['visitTime'] = response.xpath(
            '//div[@class="overview"]//div[contains(@class, "visitTime")]//span[2]/text()').extract_first()

        item['houseRecord'] = response.xpath(
            '//div[@class="overview"]//div[contains(@class, "houseRecord")]//span[2]/text()').extract_first()

        base_dic = {}
        label = response.xpath(
            '//div[@id="introduction"]//div[contains(@class,"base")]//div[contains(@class,"content")]//span/text()').extract()
        content = response.xpath(
            '//div[@id="introduction"]//div[contains(@class,"base")]//div[contains(@class,"content")]//li/text()').extract()
        for k, v in zip(label, content):
            base_dic[k] = v
        item['base'] = base_dic

        tran_dic = {}
        trans_lb = response.xpath(
            '//div[@id="introduction"]//div[contains(@class,"transaction")]//div[contains(@class,"content")]//span[1]/text()').extract()
        trans_con = response.xpath(
            '//div[@id="introduction"]//div[contains(@class,"transaction")]//div[contains(@class,"content")]//span[2]/text()').extract()
        for k, v in zip(trans_lb, trans_con):
            tran_dic[k] = v.strip()
        item['transaction'] = tran_dic

        item['tags'] = ' '.join(response.xpath(
            '//div[contains(@class, "m-content")]//div[contains(@class,"showbasemore")]//div[contains(@class,' +
            '"content")]//a/text()').extract())

        item['base_more'] = ''.join(response.xpath(
            '//div[contains(@class, "m-content")]//div[contains(@class,"showbasemore")]//div[contains(@class,' +
            '"baseattribute")]//div[@class="content"]/text()').extract()).strip().replace('\n', '').replace(' ', '')

        yield item
