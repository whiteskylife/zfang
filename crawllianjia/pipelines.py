# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



from twisted.enterprise import adbapi
import pymongo
import csv


class MySQLPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        # 从项目的配置文件中读取相应的参数
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'scrapy_default')
        cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
        cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
        cls.USER = crawler.settings.get("MYSQL_USER", 'root')
        cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", '123456')
        return cls()

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER,
                                            passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        # query.addErrback(self.handle_error)
        return item

    def insert_db(self, cursor, item):
        values = (
            item['houseRecord'], item['price'], item['unitPrice'], item['room'], item['type'], item['area'],
            item['communityName'], item['areaName'], item['visitTime'], str(item['base']), str(item['transaction']),
            item['base_more'], item['tags'], item['url']
        )
        sql = 'INSERT INTO lianjia(houseRecord, price,unitPrice,room,type,area,communityName,areaName,visitTime,' \
              'base,transaction,base_more,tags,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, values)

    # def handle_error(self, failure):
    #     print(failure)


# class MysqlTwistedPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host = settings['MYSQL_HOST'],
#             db = settings['MYSQL_DBNAME'],
#             user = settings['MYSQL_USER'],
#             passwd = settings['MYSQL_PASSWORD'],
#             charset = 'utf-8',
#             cursorclass = MySQLdb.cursors.DictCursor,
#             use_unicode = True,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
#         return cls(dbpool)
#
#
#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error)
#
#     def handle_error(self, failure):
#         print(failure)
#
#     def do_insert(self, cursor, item):
#         insert_sql = """
#
#         """
#         cursor.execute(insert_sql, (item['title']))

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
    def __init__(self):  # 初始化

        self.f = open("lianjia.csv", "w", encoding='utf-8')
        self.writer = csv.writer(self.f)
        self.writer.writerow(
            ['总价', '单价', '户型', '朝向', '面积', '小区名称', '所在区域', '看房时间', '链家编号', '基本属性',
             '交易属性', '房源特色', '房源标签', '链接']
        )

    def process_item(self, item, spider):
        # 保存为csv文件
        tencent_list = [
            item['price'], item['unitPrice'], item['room'], item['type'], item['area'], item['communityName'],
            item['areaName'],
            item['visitTime'], item['houseRecord'], item['base'], item['transaction'], item['base_more'], item['tags'],
            item['url']
        ]
        self.writer.writerow(tencent_list)
        return item

    def close_spider(self, spider):
        self.f.close()
