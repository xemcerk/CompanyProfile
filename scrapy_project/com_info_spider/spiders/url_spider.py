import scrapy
import pickle
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
import time
from ..items import UrlItem

class UrlSpider(scrapy.Spider):
    name = "url_spider"

    def start_requests(self):
        # Load company list.
        pickle_in = open("C:\\Users\Administrator\\infro_extract\\com_info_spider\\com_info_spider\\spiders\\company_list.pickle","rb")
        company_list = pickle.load(pickle_in)

        # Set up user agent.
        UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        
        # Transform cookie format.
        cookie = 'jsid=SEO-GOOGLE-ALL-SY-000001; TYCID=80be611049b511ea83b12bee8a1b51ef; undefined=80be611049b511ea83b12bee8a1b51ef; ssuid=1501493648; _ga=GA1.2.1346504665.1581085459; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2590%2595%25E5%2585%258B%25C2%25B7%25E8%25B4%259D%25E6%259D%25BE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYwMzM3ODk1MCIsImlhdCI6MTU4MTA4NTY3NSwiZXhwIjoxNjEyNjIxNjc1fQ.jR86e6n2GRzZgNiK5v9W6i3bKkElsFlZGCoF8c-k5F2KVNj5btdXSmEXwz_n8_p4XvsBxzI3DRHgTYoq7nTTzg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215603378950%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYwMzM3ODk1MCIsImlhdCI6MTU4MTA4NTY3NSwiZXhwIjoxNjEyNjIxNjc1fQ.jR86e6n2GRzZgNiK5v9W6i3bKkElsFlZGCoF8c-k5F2KVNj5btdXSmEXwz_n8_p4XvsBxzI3DRHgTYoq7nTTzg; tyc-user-phone=%255B%252215603378950%2522%255D; _gid=GA1.2.273576638.1581421484; RTYCID=80e7ec47ee5f429f82778080a9714b06; CT_TYCID=ccbf6d0a7931415cb0212bd56b11bbb1; aliyungf_tc=AQAAAFx4fzcPvgAAJ2LveHG770Rejwu5; csrfToken=8tV1ot-7C_VdTCdsYD73dW3z; bannerFlag=undefined; cloud_token=5a0ba5bf61eb4c9f9ce6310f9f11051a; cloud_utm=292463b76759404dbc5206b4f518e8f9'
        itemDict = {}
        items = cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        cookie = itemDict

        # Set up headers.
        headers = {
            'User-Agent': UserAgent,
        }

        # Assemble urls.
        search_url = 'https://www.tianyancha.com/search?key='
        urls = [search_url + company_name for company_name in company_list]
        
        # Yield requests.
        for i in range(198,len(company_list)):
            yield scrapy.Request(url=urls[i], headers=headers, cookies=cookie, callback=self.parse)

    def parse(self, response):
        # open_in_browser(response)
        
        urlItem = UrlItem()

        # scrape info url
        com_url = response.css("a.name::attr(href)").get()
        urlItem['url'] = com_url

        yield urlItem


