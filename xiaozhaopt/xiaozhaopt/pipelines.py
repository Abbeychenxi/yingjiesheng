# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import requests
import time

class XiaozhaoptPipeline(object):
    Link = 'http://backend.xiaomo.com/api/job/job'
    def process_item(self, item, spider):
        ensureItem = self._conditionalItem_(item)
        r = requests.post(self.Link, data=ensureItem)
        return item

    def _conditionalItem_(self, item):
        ensureItem = {}
        for key in ('link', 'job', 'place', 'type', 'email', 'tag', 'description'):
            if key == 'link':
                try:
                    if item['link']:
                        ensureItem[key] = self.dealInfo(item['link'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'job':
                try:
                    if item['title']:
                        ensureItem[key] = self.dealInfo(item['title'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'place':
                try:
                    if item['workPlace']:
                        ensureItem[key] = self.dealInfo(item['workPlace'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'type':
                try:
                    if item['positionType']:
                        ensureItem[key] = self.dealInfo(item['positionType']).split(':')[-1]
                        ensureItem[key] = ensureItem[key].split(u'：')[-1]
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'email':
                try:
                    if item['email']:
                        ensureItem[key] = self.dealInfo(item['email'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'tag':
                try:
                    if item['professionalLabel']:
                        ensureItem[key] = self.dealInfo(item['professionalLabel'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'description':
                try:
                    if item['description']:
                        ensureItem[key] = self.dealInfo(item['description'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'releaseTime':
                try:
                    if item['releaseTime']:
                        ensureItem[key] = self.dealInfo(item['releaseTime'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
        return ensureItem

    def dealInfo(self, temp):
        t = u''
        for index in temp:
            t += index
            t += u' '
        return t