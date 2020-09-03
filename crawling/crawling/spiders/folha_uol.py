import scrapy
from datetime import date
from crawling.crawling.items import NewsItem
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

class FolhaUolSpider(CrawlSpider):
    name = 'folha_uol'
    allowed_domains = ['folha.uol.com.br']
    start_urls = ['https://www1.folha.uol.com.br/cotidiano/coronavirus/#90',]

    def parse(self, response):
        rows = response.xpath("//body/div/main//ol/li//*[@class='c-headline__wrapper']//*[@class='c-headline__content']")
        for row in rows:
            i = NewsItem()
            i['titulo'] = row.xpath('*/h2/text()').extract()[0]
            i['link'] = row.xpath('a/@href').extract()[0]
            i['site'] = 'Folha de S.Paulo'
            i['data'] = date.today()
            yield i
            
def executaSpider():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(FolhaUolSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=False)