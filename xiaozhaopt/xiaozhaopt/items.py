# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class XiaozhaoptItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = Field()
    title = Field()
    releaseTime = Field()
    workPlace = Field()
    positionType = Field()
    position = Field()
    source = Field()
    description = Field()
    professionalLabel = Field()
    email = Field()
    validDate = Field()
    hiringNumber = Field()
