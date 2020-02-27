# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    pass

class BusinessInfoItem(scrapy.Item):
    comName = scrapy.Field() # 企业名
    telNum = scrapy.Field() # 联系电话
    email = scrapy.Field() # 邮箱
    officialSite = scrapy.Field() # 网址
    comAddr = scrapy.Field() # 地址

    registerCapital = scrapy.Field() # 注册资本
    paidupCapital = scrapy.Field() # 实缴资本
    establishmentDate = scrapy.Field() # 成立日期
    operatingStatus = scrapy.Field() # 经营状态
    uniformSocialCreditCode = scrapy.Field() # 统一社会信用代码
    businessRegNum = scrapy.Field() # 工商注册号
    taxpayerID = scrapy.Field() # 纳税人识别号
    orgCode = scrapy.Field() # 组织机构代码
    comType = scrapy.Field() # 公司类型
    industry = scrapy.Field() # 行业
    approvalDate = scrapy.Field() # 核准日期
    regAuth = scrapy.Field() # 登记机关
    operatingPeriod = scrapy.Field() # 营业期限
    taxpayerQualification = scrapy.Field() # 纳税人资质
    staffSize = scrapy.Field() # 人员规模
    insuredNum = scrapy.Field() # 参保人数
    usedName = scrapy.Field() # 曾用名
    engName = scrapy.Field() # 英文名
    regAddr = scrapy.Field() # 注册地址
    businessScope = scrapy.Field() # 经营范围
    pass

class PatentInfoItem(scrapy.Item):
    patentNum = scrapy.Field()
    softwareCopyRNum = scrapy.Field()
    patentList = scrapy.Field()
    softwareCopyRList = scrapy.Field()
    pass