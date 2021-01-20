# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class BookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ChapterItem(scrapy.Item):
    category = Field()
    bookName = Field()
    chapterName = Field()
    chapterUrl = Field()
    chapterText = Field()




