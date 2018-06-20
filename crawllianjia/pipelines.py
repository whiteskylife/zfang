# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from crawllianjia.items import lianjiaItem
import logging
import csv

# class CrawllianjiaPipeline(object):
#
#
#     def __init__(self):
#         self.items = lianjiaItem().fields
#         self.filename = open('data.csv', 'a', encoding='utf-8')
#         self.logger = logging.getLogger(__name__)
#         fieldnames = [ item for item in self.items]
#         self.__writer = csv.DictWriter(self.filename, fieldnames=fieldnames)
#         self.__writer = self.__writer.writeheader()
#
#     def process_item(self, item, spider):
#         if self.__writer.writerow(dict(item)):
#             self.logger.info('--------------存储到csv成功-----------------------！')
#         else:
#             self.logger.info('--------------存储csv失败-----------------------！')
#
#         return item
#
#     def close_spider(self, spider):
#         self.filename.close()


import pymongo
import csv


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()



class CsvPipeline(object):

    def __init__(self):#初始化

        self.f = open("lianjia.csv", "w", encoding='utf-8')
        self.writer = csv.writer(self.f)
        self.writer.writerow(
            ['总价', '单价', '户型', '朝向', '面积', '小区名称','所在区域', '看房时间',  '链家编号', '基本属性',
             '交易属性', '房源特色', '房源标签', '链接']
        )


    def process_item(self, item, spider):

        #保存为csv文件
        tencent_list = [
            item['price'], item['unitPrice'], item['room'], item['type'],item['area'], item['communityName'], item['areaName'],
            item['visitTime'], item['houseRecord'], item['base'],item['transaction'], item['base_more'], item['tags'], item['url']
        ]
        self.writer.writerow(tencent_list)
        return item


    def close_spider(self, spider):
        self.f.close()