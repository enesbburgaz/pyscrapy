#!/usr/bin/env python
# -*- coding: latin-1 -*-

from re import split
import scrapy
from scrapy import item
from ..items import PyscrapyItem
from scrapy import Request
from urllib.parse import urljoin
from urllib.parse import urlparse


class Pyscrapy2Spider(scrapy.Spider):
    name = 'pyscrapy2'
    start_urls = ['link']

    def parse(self, response):
        for href in response.xpath("//*[@id='search-app']/div/div[2]/div[2]/div[2]/div/div[@class='p-card-wrppr']/div[1]/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parsePage)

        """
        #sayfa sayisi   
        count= range(2,11)
        for x in count:
            nextPage = '/cep-telefonu?pi={0}'.format(x)
            url = response.urljoin(nextPage)
            yield scrapy.Request(url, self.parse)
        """

    def parsePage(self, response):
        yield scrapy.Request(response.url+'/yorumlar', callback=self.getComments)

    def getComments(self, response):
        item = PyscrapyItem()
        productBrand = response.xpath('//*[@id="rating-and-review-app"]/div/div[1]/div/div[1]/div[2]/h1/span[1]/text()[1]').extract()
        productName = response.xpath('//*[@id="rating-and-review-app"]/div/div[1]/div/div[1]/div[2]/h1/span[2]/text()').extract()
        item['productBrand'] = productBrand
        item['productName'] = productName

        commentCountText = response.xpath('//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[1]/div/div[2]/span[2]/text()').extract()
        commentCount = int(commentCountText[0].split()[0])
        item['commentsCount'] = commentCount

        trSupport = {'Ç': '\u00c7', 'ü': '\u00fc' }
        commentList= []
        for commentRow in response.xpath('//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[2]'):
            for i in range(0,10):
                try:
                    if commentRow.xpath('//div[@class="rnr-com-w"]/div[2]/div[1]/span[2]').extract()[i] in commentRow.xpath('//div[@class="rnr-com-w"]/div[2]/div[1]').extract()[i]:
                        buyInfo = commentRow.xpath('//div[@class="rnr-com-w"]/div[2]/div[1]/span[2]/span/text()').extract()[i]
                    else:
                        buyInfo = None
                    commentList.append({
                        'userName' : commentRow.xpath('//div[@class="rnr-com-w"]/div[2]/div[1]/span[1]/text()[1]').extract()[i],
                        'commentText' : commentRow.xpath('//div[@class="rnr-com-w"]/div[1]/div/text()').extract()[i],
                        'buyInfo' : buyInfo
                        })
                except:
                    pass
        item['comments'] = commentList
        yield item