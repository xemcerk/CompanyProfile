import scrapy
import pickle
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy_selenium import SeleniumRequest

class SeleniumSpider(scrapy.Spider):
    name = "selenium_spider"

    def start_requests(self):
        yield SeleniumRequest(url='https://www.tianyancha.com', callback=self.parse)

    def parse(self, response):
        # print(response.meta['driver'].title)
        inspect_response(response, self)


