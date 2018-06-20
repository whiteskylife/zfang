# -*- coding: utf-8 -*-

# Scrapy settings for crawllianjia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawllianjia'

SPIDER_MODULES = ['crawllianjia.spiders']
NEWSPIDER_MODULE = 'crawllianjia.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawllianjia.middlewares.CrawllianjiaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawllianjia.middlewares.CrawllianjiaDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'crawllianjia.pipelines.CrawllianjiaPipeline': 300,
   'crawllianjia.pipelines.MongoPipeline': 301,
   'crawllianjia.pipelines.CsvPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DUPEFILTER_DEBUG = True

MONGO_URI = '192.168.1.110'
MONGO_DB = 'lianjia0616'


# 替换scrapy核心调度器，用scrapy-redis的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 替换过滤规则为scrapy-redis的过滤规则
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 连接redis，每个scrapy共享爬取队列
REDIS_URL = 'redis://root:redis-pass@192.168.1.110:6379'

# 默认False，爬取完成时自动清空爬取队列和去重指纹集合，设置为True后，爬取完毕之后，request队列和dupefilter指纹信息不会被清空，会保存在redis中；如果强制中断爬虫的运行，不会自动清空；， Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# 每次启动爬虫时都会把redis请求队列指纹清空；Whether to flush redis queue on start.(default: False)
SCHEDULER_FLUSH_ON_START = False  # 本地测试设置为：True=清空，线上跑设置：False=不清空,线上要保留之前的任务队列和去重URL

# redis连接配置，下面的方式不支持配置密码，可用REDIS_URL方式配置，Specify the host and port to use when connecting to Redis (optional).
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379