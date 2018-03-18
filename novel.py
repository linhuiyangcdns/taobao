# -*- coding:utf-8

import requests
from lxml import etree
from bs4 import BeautifulSoup


class Spider(object):
    def __init__(self):
        self.headers = {
            "User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
        }
        self.url = 'http://www.shicimingju.com'
    def crawl(self):
        url = self.url + '/book'
        print url
        html = requests.get(url=url,headers=self.headers).content
        selector = etree.HTML(html)
        bookmark_links = selector.xpath('//div[@class="bookmark-list"]/ul/li/h2/a/@href')
        print(bookmark_links)
        for link in bookmark_links:
            print(link)
            link_url = self.url + link
            html2 = requests.get(url=link_url,headers=self.headers).content
            selector2 = etree.HTML(html2)
            book_mulu_links = selector2.xpath('//div[@class="book-mulu"]/ul/li/a/@href')
            book_title = selector2.xpath('//div[@class="book-header"]/h1/text()')
            book_title = ''.join(book_title)
            #print(book_title)
            #self.writeData(book_title)
            for mulu_link in book_mulu_links:
                mulu_url = self.url + mulu_link
                print(mulu_url)
                html3 = requests.get(url=mulu_url,headers=self.headers).content
                #html3.encoding('utf-8')
                soup = BeautifulSoup(html3,'html.parser')
                title = soup.h1
                body = soup.select('p')
                #print(title.encode('utf-8'))
                body = ','.join(str(v) for v in body)
                book =body.replace('<p>',"").replace('</p>',"")
                #print(book)
                self.writeData(book_title,title,book)

    def writeData(self,book_title,title,book):
        filename = book_title + '.text'
        filename = open(filename,'a')
        filename.write(title.encode('utf-8') + '\n')
        filename.write(book + ';\n')


if __name__ == "__main__":

    spider = Spider()
    spider.crawl()




