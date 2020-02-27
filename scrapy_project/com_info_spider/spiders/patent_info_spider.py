import scrapy
import pandas as pd
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from ..items import PatentInfoItem


class PatentInfoSpider(scrapy.Spider):
    name = "patent_info_spider"

    def start_requests(self):
        # Load company url list.
        company_url_list = pd.read_json('C:\\Users\\Administrator\\\infro_extract\\com_info_spider\\company_url_list.json')['url'].to_list()

        # Set up user agent.
        UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        
        # Transform cookie format.
        cookie = 'jsid=SEO-GOOGLE-ALL-SY-000001; TYCID=80be611049b511ea83b12bee8a1b51ef; undefined=80be611049b511ea83b12bee8a1b51ef; ssuid=1501493648; _ga=GA1.2.1346504665.1581085459; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2590%2595%25E5%2585%258B%25C2%25B7%25E8%25B4%259D%25E6%259D%25BE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYwMzM3ODk1MCIsImlhdCI6MTU4MTA4NTY3NSwiZXhwIjoxNjEyNjIxNjc1fQ.jR86e6n2GRzZgNiK5v9W6i3bKkElsFlZGCoF8c-k5F2KVNj5btdXSmEXwz_n8_p4XvsBxzI3DRHgTYoq7nTTzg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215603378950%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYwMzM3ODk1MCIsImlhdCI6MTU4MTA4NTY3NSwiZXhwIjoxNjEyNjIxNjc1fQ.jR86e6n2GRzZgNiK5v9W6i3bKkElsFlZGCoF8c-k5F2KVNj5btdXSmEXwz_n8_p4XvsBxzI3DRHgTYoq7nTTzg; tyc-user-phone=%255B%252215603378950%2522%255D; _gid=GA1.2.273576638.1581421484; aliyungf_tc=AQAAAFx4fzcPvgAAJ2LveHG770Rejwu5; csrfToken=8tV1ot-7C_VdTCdsYD73dW3z; bannerFlag=true; RTYCID=1f32c209898d49109e25f1300364e245; CT_TYCID=e68654a35c0149b6b0e86c51772f70ae; cloud_token=af297931e1ec416bb03d97ff9d8bd97e'
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

        null_list = [3,31,71,119,120,132,165,170,171,176,183,195,204,206,209,210]

        # Yield requests.
        for i in range(140,len(company_url_list)):
            request = scrapy.Request(url=company_url_list[i], headers=headers, cookies=cookie, callback=self.parse, dont_filter=True)
            if i in null_list:
                request.meta['isNull'] = True
            else:
                request.meta['isNull'] = False
            yield request

    def parse(self, response):
        
        patentInfoItem = PatentInfoItem()

        if not response.meta['isNull']:
            patentInfoItem['patentNum'] = response.xpath('//*[@id="nav-main-patentCount"]/span[2]/text()').get()
            patentInfoItem['softwareCopyRNum'] = response.xpath('//*[@id="nav-main-cpoyRCount"]/span[2]/text()').get()
            patentList = []
            softwareCopyRList = []

            # 专利
            # 申请公布日
            appliAnncDateList = response.xpath('//*[@id="_container_patent"]/table/tbody//tr/td[2]//text()').getall()
            # 专利名称
            patentNameList = response.xpath('//*[@id="_container_patent"]/table/tbody//tr/td[3]//text()').getall()
            # 申请号
            appliNumList = response.xpath('//*[@id="_container_patent"]/table/tbody//tr/td[4]//text()').getall()
            # 申请公布号
            appliAnncNumList = response.xpath('//*[@id="_container_patent"]/table/tbody//tr/td[5]//text()').getall()
            # 专利类型
            patentTypeList = response.xpath('//*[@id="_container_patent"]/table/tbody//tr/td[6]//text()').getall()
            # 详情链接
            moreInfoRefList = response.xpath('//*[@id="_container_patent"]/table/tbody//tr/td[7]//@href').getall()
            for i in range(len(appliAnncDateList)):
                patent = {}
                patent['appliAnncDate'] = appliAnncDateList[i]
                patent['patentName'] = patentNameList[i]
                patent['appliAnncNum'] = appliAnncNumList[i]
                patent['patentType'] = patentTypeList[i]
                patent['moreInfoRef'] = moreInfoRefList[i]
                patentList.append(patent)
            patentInfoItem['patentList'] = patentList

            # 软件著作权
            # 登记批准日期
            regApprDateList = response.xpath('//*[@id="_container_copyright"]/table//tbody//tr/td[2]/span/text()').getall()
            # 软件全称
            softwareFullNameList = response.xpath('//*[@id="_container_copyright"]/table//tbody//tr/td[3]/span/text()').getall()
            # 软件简称
            softwareAbbrList = response.xpath('//*[@id="_container_copyright"]/table//tbody//tr/td[4]/span/text()').getall()
            # 登记号
            regNumList = response.xpath('//*[@id="_container_copyright"]/table//tbody//tr/td[5]/span/text()').getall()
            # 分类号
            classNumList = response.xpath('//*[@id="_container_copyright"]/table//tbody//tr/td[6]/span/text()').getall()
            for i in range(len(regNumList)):
                softwareCopyR = {}
                softwareCopyR['regApprDate'] = regApprDateList[i]
                softwareCopyR['softwareFullName'] = softwareFullNameList[i]
                softwareCopyR['softwareAbbr'] = softwareAbbrList[i]
                softwareCopyR['regNum'] = regNumList[i]
                softwareCopyR['classNum'] = classNumList[i]
                softwareCopyRList.append(softwareCopyR)
            patentInfoItem['softwareCopyRList'] = softwareCopyRList

        yield patentInfoItem
        # inspect_response(response, self)
