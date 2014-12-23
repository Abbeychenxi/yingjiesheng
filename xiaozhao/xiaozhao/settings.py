# -*- coding: utf-8 -*-

# Scrapy settings for xiaozhao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xiaozhao'

SPIDER_MODULES = ['xiaozhao.spiders']
NEWSPIDER_MODULE = 'xiaozhao.spiders'

COOKIES_ENABLED = False


DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'xiaozhao.middlewares.rotate_useragent.RotateUserAgentMiddleware': 400,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        'xiaozhao.middlewares.Proxyware.ProxyMiddleware': 100,
        'xiaozhao.middlewares.google_cache.GoogleCacheMiddleware': 50,
    }

DOWNLOAD_DELAY = 2


ITEM_PIPELINES = ['xiaozhao.pipelines.XiaozhaoPipeline']


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xiaozhao (+http://www.yourdomain.com)'
USER_AGENT = ''
