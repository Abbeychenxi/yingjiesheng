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
        'scrapy.middlerware.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'xiaozhao.middlerware.rotate_useragent.RotateUserAgentMiddleware': 400
    }

DOWNLOAD_DELAY = 1


ITEM_PIPELINES = ['xiaozhao.pipelines.XiaozhaoPipeline']


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xiaozhao (+http://www.yourdomain.com)'
USER_AGENT = ''
