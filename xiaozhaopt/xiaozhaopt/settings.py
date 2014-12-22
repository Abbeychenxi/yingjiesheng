# -*- coding: utf-8 -*-

# Scrapy settings for xiaozhaopt project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xiaozhaopt'

SPIDER_MODULES = ['xiaozhaopt.spiders']
NEWSPIDER_MODULE = 'xiaozhaopt.spiders'

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
        'scrapy.middlerware.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'xiaozhaopt.middlerware.rotate_useragent.RotateUserAgentMiddleware': 400
    }

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = ['xiaozhaopt.pipelines.XiaozhaoptPipeline']



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xiaozhaopt (+http://www.yourdomain.com)'
USER_AGENT = ''