# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import json
from tubatu.items import TubatuItem


class SpiderSpider(CrawlSpider):
    name = 'tubatu'
    start_url_domain = 'xiaoguotu.to8to.com'
    allowed_domains = ['to8to.com']
    start_urls = ['http://xiaoguotu.to8to.com/tuce/']

    rules = (
        Rule(LinkExtractor(allow=r'tuce/p_\d+.html'), callback='parse_list', follow=True),
    )

    def parse_list(self, response):
        selector = Selector(response)
        items_selector = selector.xpath('//div[@class="xmp_container"]//div[@class="item"]')
        for item_selector in items_selector:
            cid = item_selector.xpath('./div/a/@href').extract()[0][-13:-6]
            title = item_selector.xpath('./div/a/@title').extract()[0]
            next_url = ('http://' + self.start_url_domain + '/case/list?a2=0&a12=&a11={cid}&a1=0&a17=1').format(cid=cid)
            yield scrapy.Request(url = next_url,callback=self.parse_content,meta={'cid':cid , 'title':title})

    def parse_content(self,response):
        cid = response.meta['cid']
        title = response.meta['title']
        try :
            data = json.loads(response.text)
        except:
            print(response.text)
        data_image_lists = data['dataImg']
        data_album_lists = None
        for _data_img in data_image_lists:
            if _data_img['cid'] == cid:
                data_album_lists = _data_img['album']
                break
        for data_album in data_album_lists:
            data_img = data_album['1']
            img_url = 'http://xiaoguotu.to8to.com/tuce/{short_name}'.format(short_name= data_img['s'])
            img_name = data_img['t']
            html_url = response.url
            item = TubatuItem()
            item['title'] =title
            item['html_url'] = html_url
            item['image_name'] = img_name
            item['image_url'] = img_url
            yield item

