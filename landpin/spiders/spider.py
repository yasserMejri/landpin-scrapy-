import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from landpin.items import ChainItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    start_urls = ['https://landpin.com/transaction-history/?fwp_state=fl']
    state= ''
    pgnum = 1
    end = False

    def __init__(self, state = '', *args, **kwargs):
        self.state = state

    def start_requests(self):
        url = 'https://landpin.com/transaction-history/?fwp_state='+self.state+'&fwp_paged='+str(self.pgnum)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        esc = self.validate(response.xpath("//p[contains(@class, 'woocommerce-info')]/text()"))

        if esc == 'No products were found matching your selection.':
            return

        urls = response.xpath('//li/a[@class="woocommerce-LoopProduct-link"]/@href').extract()

        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse_item)

        self.pgnum = self.pgnum + 1
        url = 'https://landpin.com/transaction-history/?fwp_state='+self.state+'&fwp_paged='+str(self.pgnum)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):

        item = ChainItem()

        item['url'] = response.url
        item['state'] = self.validate(response.xpath('//td[@class="meta-label"][text()="State"]/following-sibling::td/text()'))
        item['county'] = self.validate(response.xpath('//td[@class="meta-label"][text()="County"]/following-sibling::td/text()'))
        item['apn'] = self.validate(response.xpath('//td[@class="meta-label"][text()="APN or Other ID"]/following-sibling::td/text()'))
        item['gps'] = self.validate(response.xpath('//td[@class="meta-label"][text()="GPS"]/following-sibling::td/text()'))
        item['size'] = self.validate(response.xpath('//td[@class="meta-label"][text()="Size (Acres)"]/following-sibling::td/text()'))
        item['price'] = self.validate(response.xpath("//span[contains(@class, 'woocommerce-Price-amount')]/text()"))
        item['zoning'] = self.validate(response.xpath('//td[@class="meta-label"][text()="Zoning"]/following-sibling::td/text()'))
        item['legal_description'] = self.validate(response.xpath('//td[@class="meta-label"][text()="Legal Description"]/following-sibling::td/text()')).replace('\n',' ')

        yield item

    def validate(self, data):
        try:
            return data.extract_first().strip()
        except:
            return ''

