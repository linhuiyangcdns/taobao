# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qichezhijia.items import QichezhijiaItem



class QicheSpider(CrawlSpider):
    name = 'qiche'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://www.autohome.com.cn/news/']
    #page_links = LinkExtractor(allow=r'news/\d+/')
    contentlinks = LinkExtractor(allow=r'news/\d+?/\d+?.html#pvareaid=\d+')
    rules = (
        #Rule(page_links),
        Rule(contentlinks,callback="parse_item",follow=True),
    )

   # def parse(self, response):

    def parse_item(self, response):
        item = QichezhijiaItem()
        item['name']= self.get_name(response)
        item['time'] = self.get_time(response)
        item['source'] = self.get_source(response)
        item['type'] = self.get_type(response)
        item['editor'] = self.get_editor(response)
        item['content'] = self.get_content(response)
        yield item

    def get_name(self,response):
        name = response.xpath('//div[@class="row"]/div/div/h1/text()').extract()
        if len(name):
            name = name[0]
        else:
            name = "NULL"
        return name

    def get_time(self,response):
        time = response.xpath('//div[@class="row"]/div/div/div[1]/span[1]/text()').extract()
        if len(time):
            time = time[0]
        else:
            time = "NULL"
        return time

    def get_source(self,response):
        source = response.xpath('//div[@class="row"]/div/div/div[1]/span[2]/text()').extract()
        if len(source):
            source = source[0]
        else:
            source = "Null"
        return source

    def get_type(self,response):
        type = response.xpath('//div[@class="row"]/div/div/div[1]/span[3]/text()').extract()
        if len(type):
            type = type[0]
        else:
            type = "NULL"
        return type

    def get_editor(self,response):
        editor = response.xpath('//div[@class="row"]/div/div/div[1]/div/a/text()').extract()
        if len(editor):
            editor = editor[0]
        else:
            editor = "NULL"
        return editor

    def get_content(self,response):
        content = response.xpath('//div/div[@id="articleContent"]/p/text()').extract()
        if len(content):
            content= ' '.join(content)
        else:
            content = "NULL"
        return content