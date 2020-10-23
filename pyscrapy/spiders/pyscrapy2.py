import scrapy
from ..items import PyscrapyItem
from scrapy import Request
from urllib.parse import urljoin
from urllib.parse import urlparse


class Pyscrapy2Spider(scrapy.Spider):
    name = 'pyscrapy2'
    start_urls = ['link']

    def parse(self, response):
        for href in response.xpath("//*[@id='search-app']/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parsePage)

        """   
        nextPage = response.xpath("//div[contains{@class, 'unified'}]/a[contains{@class, 'next'}]/@href")
        if nextPage:
            url = response.urljoin(nextPage[0].extract())
            yield scrapy.Request(url, self.parse)
        """

    def parsePage(self, response):
        item = PyscrapyItem()
        productTitle = response.xpath("//*[@id='product-detail-app']/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span/text()").extract()

        item['productTitle'] = productTitle
        yield item