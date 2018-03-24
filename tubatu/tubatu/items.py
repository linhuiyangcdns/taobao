# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TubatuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    html_url = scrapy.Field()  # 网页链接
    image_name = scrapy.Field()  # 图片名称
    image_url = scrapy.Field()  # 图片链接