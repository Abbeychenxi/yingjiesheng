__author__ = 'Abbey'

import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from xiaozhao.items import XiaozhaoItem
import re

class yJS(Spider):
    name = 'YJS'
    allowed_domains = ['yingjiesheng.com']

    start_urls = []
    def __init__(self):
        with open('links', 'r') as f:
            oneString = f.read()
        links = oneString.split(' ')
        for link in links:
            self.start_urls.append(link)

    def parse(self, response):
        sel = Selector(response)
        item = XiaozhaoItem()
        div = sel.xpath('//div[@class="mleft"] | //div[@class="com_mleft"]')
        item['title'] = div.xpath('h1/text() | div[@class="com"]/h2/a/text()').extract()
        div_info = div.xpath('div[@class="info clearfix"]')
        lis = div_info.xpath('ol')
        for index, li in enumerate(lis.xpath('li')):
            if index == 0:
                item['releaseTime'] = li.xpath('u/text()').extract()
            elif index == 1:
                item['workPlace'] = li.xpath('u/text()').extract()
            elif index == 2:
                item['positionType'] = li.xpath('u/text()').extract()
            elif index == 3:
                item['source'] = li.xpath('u/text()').extract()
            elif index == 4:
                item['position'] = li.xpath('u/text()').extract()
            else:
                item['postion'] = []
        professionalLabel = div.xpath('div[@style="margin-top:10px; overflow:hidden"]/a/text()').extract()
        if professionalLabel:
            item['professionalLabel'] = professionalLabel
        else:
            item['professionalLabel'] = []
        info = sel.xpath('//div[@class="jobIntro"] | //div[@class="job_list"]')
        description = info.xpath('.//a/text() | .//p/text() | .//div/text() | .//span/text()').extract()
        item['description'] = description
        pattern = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
        item['email'] = []
        for index in description:
            match = pattern.match(index)
            if match:
                item['email'].append(match.group())
        return item