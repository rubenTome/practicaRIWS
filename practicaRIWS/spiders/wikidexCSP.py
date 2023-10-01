from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class wikidexCSP(CrawlSpider):
    name = "wikidexx"
    allowed_domains = ["wikidex.net"]
    start_urls = ["https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon"]
    rules = (Rule(LinkExtractor(allow = "Bulbasaur"), 
                  callback = "parse_item", 
                  follow = False),)

    def parse_item(self, response):
        print("A\nAA\nAAA\nAAAA\nAAAAA")
