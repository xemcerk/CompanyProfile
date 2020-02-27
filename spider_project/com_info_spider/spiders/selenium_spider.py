import scrapy
import pickle
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy_selenium import SeleniumRequest

class SeleniumSpider(scrapy.Spider):
    name = "selenium_spider"

    start_urls = ['https://www.tianyancha.com']

    def parse(self, response):
        inspect_response(response)


