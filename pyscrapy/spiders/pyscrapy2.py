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
  
        count= range(2,11)
        for x in count:
            nextPage = '/cep-telefonu?pi={0}'.format(x)
            url = response.urljoin(nextPage)
            yield scrapy.Request(url, self.parse)
        

    def parsePage(self, response):
        yield scrapy.Request(response.url+'/yorumlar', callback=self.getComments)

    def getComments(self, response):
        productBrand = response.xpath('//*[@id="rating-and-review-app"]/div/div[1]/div/div[1]/div[2]/h1/span[1]/text()').extract()
        productName = response.xpath('//*[@id="rating-and-review-app"]/div/div[1]/div/div[1]/div[2]/h1/span[2]/text()').extract()
        userName = response.xpath('//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[2]/div[@class="rnr-com-w"]/div[2]/div[1]/span[1]/text()[1]').extract()
        comments= response.xpath('//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[2]/div[@class="rnr-com-w"]/div[1]/div/text()').extract()
        buyInfo = response.xpath('//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[2]/div[@class="rnr-com-w"]/div[2]/div[1]/span[2]/span/text()').extract()        
        
        for item in zip(productBrand, productName, userName, comments, buyInfo):
            scraped_data = {
                'Product Brand': item[0],
                'Product Name': item[1],
                'User Name': item[2],
                'Comment': item[3],
                'Buy Info': item[4]
            }
            yield scraped_data