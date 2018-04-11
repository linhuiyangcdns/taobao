# -*- coding: utf-8 -*-
import scrapy
import re
from taobao.items import TaobaoItem
import urllib,urllib2,requests

class TaobaopcSpider(scrapy.Spider):
    """
    作用：爬取淘宝女装信息
    """
    name = 'taobaopc'
    #allowed_domains = ['taobao.com']
    start_urls = ['https://www.taobao.com/']
    key = 0
    url = "https://s.taobao.com/search?q=%E5%A5%B3%E8%A3%85&s="
    start_urls = [url + str(key)]

    # def parse(self, response):
    #     #url = 'https://s.taobao.com/search?q=%E5%A5%B3%E8%A3%85&s='
    #     #key = 0
    #     #full_url = url + str(key)
    #     #yield scrapy.Request(full_url, callback=self.page)
    #     if self.key <= 4356:
    #         self.key += 44
    #         yield scrapy.Request(url+ key,callback=self.page)

    def parse(self,response):
        body = response.body.decode('utf-8')
        url_id = '"nid":"(.*?)",'
        #sellerId= '"user_id":"(.*?)"'
        all_ids = re.compile(url_id).findall(body)

        for id in all_ids:
            url = "https://item.taobao.com/item.htm?id=" + str(id)
            #如果是天猫自动转换
            yield scrapy.Request(url,callback=self.content, meta={'id':id,})
        if self.key <= 4356:
            self.key += 44
            yield scrapy.Request(self.url+ str(self.key),callback=self.parse)

    def content(self,response):
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
        }
        url = response.url
        #print url
        id = response.meta['id']
        domain_url = 'https://(.*?).com'
        subdomain = re.compile(domain_url).findall(url)
        if subdomain[0] != 'item.taobao':
            title = response.xpath('//div[@class="tb-property"]/div/div/h1/text()').extract()[0]
            price = response.xpath('//div[@class="tm-promo-price"]/span/text()').extract()[0]
            #comment = response.xpath('//div[@id="J_TabBarBox"]/ul/li[2]/a/em/text()').extract()[0]
            sellerid = response.xpath('//div[@id="shop-info"]/div/input[2]/@value').extract()[0]
            url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={itemid}&sellerId={sellerid}&order=1'.format(itemid=id,sellerid=sellerid)
            #html = requests.get(url, headers=headers).content
            request = urllib2.Request(url,headers=headers)
            html = urllib2.urlopen(request).read()
            total = '"total":(.*?),'
            comment = re.compile(total).findall(html)
        else:
            title = response.xpath('//div[@class="tb-property tb-property-x"]/div/div/h3/text()').extract()[0]
            # try:
            #     price = response.xpath('//div[@class="tb-property-cont"]/div/div/div/strong/em[2]/text()').extract()[0]
            # except:
            #     price = None
            try:
                js_url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={itemid}&sellerId={sellerid}&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,amountRestriction,couponActivity,soldQuantity,originalPrice,tradeContract".format(itemid=id,sellerid=sellerid)
                headers = {
                    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
                    "referer": url,
                    "cookie": "thw=cn; cna=v+ABE/RY1jUCATywMStcNVSV; t=49606a6db44797246f57d3ca4991368f; enc=gMidmIcD2PiSIe1S1Ez6B2TwJGApCXZsjO5bL0Tp6w%2BsutpqV190kH3Un5O1qhgujA%2BTqlTubzmRVXqp2iAUrQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; v=0; cookie2=38240f62644cd92e84f72632497b4d5d; _tb_token_=73e3ee134ebed; mt=ci%3D-1_1; isg=BKWlmCYbE2o6-3d7yvtuqPActGEfSlhm7EDATaeLDlzuvsEwbDFjRRY_TCTIvnEsreferer:https://item.taobao.com/item.htm?id=549186106859&ns=1&abbucket=8",
                }
                html = requests.get(url, headers=headers).content
                price= '"price":"(.*?),"'
                price = re.compile(price).findall(html)
            except:
                price = response.xpath('//div[@class="tb-property-cont"]/strong/em[@class="tb-rmb-num"]/text()').extract()[0]
                #促销价格在js文件中，如果未打开使用原始价格先凑合一下
            #comment = response.xpath('//div[@class="tb-tabbar-mid-wrap tb-clear"]/div/ul/li[2]/a/em/text()').extract()[0]
            sellerid = response.xpath('//div[@id="J_Pine"]/@data-sellerid').extract()[0]
            url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId={auctionid}&userNumId={userid}&currentPageNum=1'.format(auctionid=id,userid=sellerid)
            html = requests.get(url, headers=headers).content
            total = '"total":(.*?),'
            comment = re.compile(total).findall(html)

        item = TaobaoItem()
        item['title'] = title
        item['price'] = price
        item['link'] = url
        item['comment']= comment[0]
        yield item