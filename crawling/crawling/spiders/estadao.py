# import sys
# sys.path.append('C:\\Users\\Eduardo Monita\\Desktop\\APS\\best_news\\crawling')

import scrapy
from scrapy import Spider
from datetime import date
from crawling.crawling.items import NewsItem
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

class EstadaoSpider(CrawlSpider):
    name = 'estadao'
    allowed_domains = ['economia.estadao.com.br']
    start_urls = ['https://economia.estadao.com.br/',]

    def parse(self, response):
        rows = response.xpath("//*[@class='box ']")
        for row in rows:
            news_item = NewsItem()
            if not(row.xpath('a[1]/h3/text()').extract() == []):
                news_item['titulo'] = row.xpath('a[1]/h3/text()').extract()[0]
                news_item['link'] = row.xpath('a[1]/@href').extract()[0]
                news_item['site'] = 'Estadão'
                news_item['data'] = date.today()
            
                yield news_item
                
def executaSpider():    
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(EstadaoSpider)
        reactor.stop()

    return crawl()
    # reactor.run(installSignalHandlers=False)