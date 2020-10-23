# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PyscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    productTitle = scrapy.Field()
    commentText = scrapy.Field()
    commentName = scrapy.Field()
    buyInfo = scrapy.Field()
