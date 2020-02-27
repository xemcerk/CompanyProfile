import scrapy
import pandas as pd
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from ..items import BusinessInfoItem


class DetailInfoSpider(scrapy.Spider):
    name = "detail_info_spider"

    def start_requests(self):
        # Load company url list.
        company_url_list = pd.read_json('C:\\Users\\Administrator\\\infro_extract\\com_info_spider\\company_url_list.json')['url'].to_list()

        # Set up user agent.
        UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        
        # Transform cookie format.
        cookie = 'jsid=SEO-GOOGLE-ALL-SY-000001; TYCID=80be611049b511ea83b12bee8a1b51ef; undefined=80be611049b511ea83b12bee8a1b51ef; ssuid=1501493648; _ga=GA1.2.1346504665.1581085459; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2590%2595%25E5%2585%258B%25C2%25B7%25E8%25B4%259D%25E6%259D%25BE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYwMzM3ODk1MCIsImlhdCI6MTU4MTA4NTY3NSwiZXhwIjoxNjEyNjIxNjc1fQ.jR86e6n2GRzZgNiK5v9W6i3bKkElsFlZGCoF8c-k5F2KVNj5btdXSmEXwz_n8_p4XvsBxzI3DRHgTYoq7nTTzg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215603378950%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYwMzM3ODk1MCIsImlhdCI6MTU4MTA4NTY3NSwiZXhwIjoxNjEyNjIxNjc1fQ.jR86e6n2GRzZgNiK5v9W6i3bKkElsFlZGCoF8c-k5F2KVNj5btdXSmEXwz_n8_p4XvsBxzI3DRHgTYoq7nTTzg; tyc-user-phone=%255B%252215603378950%2522%255D; _gid=GA1.2.273576638.1581421484; RTYCID=80e7ec47ee5f429f82778080a9714b06; CT_TYCID=ccbf6d0a7931415cb0212bd56b11bbb1; aliyungf_tc=AQAAAFx4fzcPvgAAJ2LveHG770Rejwu5; csrfToken=8tV1ot-7C_VdTCdsYD73dW3z; bannerFlag=true; cloud_token=0782299ce4874d06bbec843a5e1b88a6; _gat_gtag_UA_123487620_1=1'
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

        # Yield requests.
        # for i in range(1):
        #     yield scrapy.Request(url=company_url_list[210], headers=headers, cookies=cookie, callback=self.parse, dont_filter=True)
        urls = [
            'https://www.tianyancha.com/company/3100516616',
            'https://www.tianyancha.com/company/3097983747',
            'https://www.tianyancha.com/company/2575966077'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, cookies=cookie, callback=self.parse, dont_filter=True)

    def parse(self, response):
        bussInfoItem = BusinessInfoItem()
        bussInfoItem['comName'] = response.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[1]/h1/text()').get()
        bussInfoItem['telNum'] = response.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[1]/div[1]/span[2]/text()').get()
        bussInfoItem['email'] = response.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[1]/div[2]/span[2]/text()').get()
        bussInfoItem['officialSite'] = response.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[2]/div[1]/a/text()').get()
        bussInfoItem['comAddr'] = response.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[2]/div[2]/div/div/text()').get()

        bussInfoItem['registerCapital'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div/text()').get()
        bussInfoItem['paidupCapital'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]/text()').get()
        bussInfoItem['establishmentDate'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/div/text()').get()
        bussInfoItem['operatingStatus'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]/text()').get()
        bussInfoItem['uniformSocialCreditCode'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()').get()
        bussInfoItem['businessRegNum'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()').get()
        bussInfoItem['taxpayerID'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[2]/text()').get()
        bussInfoItem['orgCode'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[4]/text()').get()
        bussInfoItem['comType'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[2]/text()').get()
        bussInfoItem['industry'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()').get()
        bussInfoItem['approvalDate'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[2]/text()').get()
        bussInfoItem['regAuth'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[4]/text()').get()
        bussInfoItem['operatingPeriod'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/span/text()').get()
        bussInfoItem['taxpayerQualification'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[4]/text()').get()
        bussInfoItem['staffSize'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[2]/text()').get()
        bussInfoItem['insuredNum'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[4]/text()').get()
        bussInfoItem['usedName'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[2]/span/text()').get()
        bussInfoItem['engName'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[4]/text()').get()
        bussInfoItem['regAddr'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[10]/td[2]/text()').get()
        bussInfoItem['businessScope'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[11]/td[2]/span/text()').get()

        yield bussInfoItem
        # inspect_response(response, self)