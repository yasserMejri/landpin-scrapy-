# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):    
    url = Field()
    state = Field()
    county = Field()
    apn = Field()
    gps = Field()
    size = Field()
    price = Field()
    zoning = Field()
    legal_description = Field()
