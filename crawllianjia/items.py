# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class lianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'page1'

    price = Field()
    unitPrice = Field()

    room = Field()
    type = Field()
    area = Field()

    communityName = Field()     # 小区名称
    areaName = Field()          # 所在区域
    visitTime = Field()         # 看房时间
    houseRecord = Field()       # 链家编号

    base = Field()              # 基本属性
    transaction = Field()       # 交易属性

    base_more = Field()             # 房源特色

    tags = Field()                  # 房源标签

    url = Field()

    # base_attribute = Field()         # 户型介绍
    # tax_detail = Field()             # 税费解析
    # around = Field()             # 周边配套
    # traffic = Field()             # 交通出行
    # suit_person = Field()             # 适宜人群
    # sale_point = Field()             # 核心卖点

    pass
