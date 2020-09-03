import scrapy
from datetime import date
from crawling.crawling.items import NewsItem
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

class NexoJornalSpider(CrawlSpider):
    name = 'nexojornal'
    allowed_domains = ['nexojornal.com.br']
    start_urls = ['https://www.nexojornal.com.br/tema/Tecnologia',]

    def parse(self, response):
        rows = response.xpath('//*[@id="app"]/main/div[1]/ul/li')
        for row in rows:
            i = NewsItem()
            i['titulo'] = row.xpath('article/h4/a/@title').extract()[0]
            i['link'] = 'https://www.nexojornal.com.br' + row.xpath('article/h4/a/@href').extract()[0]
            i['site'] = 'Nexo'
            i['data'] = date.today()
            yield i

def executaSpider():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(NexoJornalSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=False)