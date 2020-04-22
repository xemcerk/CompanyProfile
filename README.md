# 企业画像数据库

## 使用说明（python api）

#### 参考链接：

1.  pymongo接口手册：https://api.mongodb.com/python/current/index.html
2.  MongoDB CRUD操作手册：https://docs.mongodb.com/manual/crud/

#### 调取所有数据

```python
import pymongo
import pandas as pd

# 连接到mongo server
client = pymongo.MongoClient(host='10.108.210.101')

# 提取数据库TechBigData中 集合CompanyProfile的所有数据
df = pd.DataFrame(list(client.TechBigData.CompanyProfile.find()))
```

#### 添加新值域

```python
# 创建test数据库与TestCollection集合
test_db = client.test
test_clc = test_db['TestCollection']

# 编写测试样例
test_docs = [
    {"f1":"a"},
    {"f1":"b"}
]

# 插入测试样例
test_clc.insert_many(test_docs)

# 获取欲插入的新field的值
new_field_values = [1,2]

# 获取TestCollction中的_id列表
id_list = list(test_clc.find({},{"_id":1}))

# 逐样例插入新值域
for i,id in enumerate(id_list):
    test_clc.update_one({"_id":id_list[i]['_id']},{"$set":{"new_field":new_field_values[i]}})
print(list(test_clc.find({})))
```

```shell
[{'_id': ObjectId('5e590d3cba53968d166f54b5'), 'f1': 'a', 'new_field': 1},
 {'_id': ObjectId('5e590d3cba53968d166f54b6'), 'f1': 'b', 'new_field': 2}]
```



## 数据字段说明

### 1.集合TechBigData.CompanyProfile

| 字段         | 字段类型 | 字段说明  | 备注                                        |
| --------------------- | ------ | ------------- | ----------------------------------------------- |
| staffNumRange | String | varchar(200) | 人员规模 |
| fromTime              | Number | 毫秒数        | 经营开始时间                                    |
| type                  | Number |               | 法人类型，1 人 2 公司                           |
| bondName              | String | varchar(20)   | 股票名                                          |
| id                    | Number |               | 企业id                                          |
| isMicroEnt            | Number |               | 是否是小微企业 0不是 1是                        |
| usedBondName          | String | varchar(20)   | 股票曾用名                                      |
| regNumber             | String | varchar(31)   | 注册号                                          |
| percentileScore       | Number | 万分制        | 企业评分                                        |
| regCapital            | String | varchar(50)   | 注册资本                                        |
| name                  | String | varchar(255)  | 企业名                                          |
| regInstitute          | String | varchar(255)  | 登记机关                                        |
| regLocation           | String | varchar(255)  | 注册地址                                        |
| industry              | String | varchar(255)  | 行业                                            |
| approvedTime          | Number | 毫秒数        | 核准时间                                        |
| socialStaffNum        | Number |               | 参保人数                                        |
| tags                  | String | varchar(255)  | 企业标签                                        |
| taxNumber             | String | varchar(255)  | 纳税人识别号                                    |
| businessScope         | String | varchar(4091) | 经营范围                                        |
| property3             | String | varchar(255)  | 英文名                                          |
| alias                 | String | varchar(255)  | 简称                                            |
| orgNumber             | String | varchar(31)   | 组织机构代码                                    |
| regStatus             | String | varchar(31)   | 企业状态                                        |
| estiblishTime         | Number | 毫秒数        | 成立日期                                        |
| bondType              | String | varchar(31)   | 股票类型                                        |
| legalPersonName       | String | varchar(120)  | 法人                                            |
| toTime                | Number | 毫秒数        | 经营结束时间                                    |
| actualCapital         | String | varchar(50)   | 实收注册资金                                    |
| companyOrgType        | String | varchar(127)  | 企业类型                                        |
| base                  | String | varchar(31)   | 省份简称                                        |
| creditCode            | String | varchar(255)  | 统一社会信用代码                                |
| historyNames          | String | varchar(255)  | 曾用名                                          |
| bondNum               | String | varchar(20)   | 股票号                                          |
| regCapitalCurrency    | String | varchar(10)   | 注册资本币种  人民币 美元 欧元 等(暂未使用)     |
| actualCapitalCurrency | String | varchar(10)   | 实收注册资本币种  人民币 美元 欧元 等(暂未使用) |
| revokeDate            | Number | 毫秒数        | 吊销日期                                        |
| revokeReason          | String | varchar(500)  | 吊销原因                                        |
| cancelDate            | Number | 毫秒数        | 注销日期                                        |
| cancelReason          | String | varchar(500)  | 注销原因                                        |
| topicVec | list |  | 根据经营范围进行主题建模得到的结果向量 |
| is_in_patent_graph | Boolean | | 该企业是否存在于专利图谱中 |

### 2. 集合TechBigData.LegalPerson

1.  name：企业名称
2.  humanName：法人姓名
3.  items：法人所持有的全部企业的列表
    1.  regStatus：企业营业状态（可选"开业"、“存续（在营、开业、在册）” 或 ”注销“）
    2.  estiblishTime：成立时间
    3.  regCapital：注册资产
    4.  name：企业名称
    5.  type：上述法人在公司承担的职务
    6.  base：地点
    7.  cid：天眼查中该企业对应id
4.  total：法人所持有的全部企业的计数