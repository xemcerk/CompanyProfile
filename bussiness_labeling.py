# %%
import pymongo
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import numpy as np
import re

import sys
sys.path.append('..')

# 链接mongodb并读取企业经营范围
print("链接mongodb并读取企业经营范围")
client = pymongo.MongoClient(host='49.234.215.201', port=32919)
cp = client.TechBigData.CompanyProfile
#%%
df = pd.DataFrame(list(cp.find({},{"_id":1, "businessScope":1})))
df = df.dropna()
scope_str_list = df['businessScope'].to_list()
id_list = df['_id'].to_list()
#%%
# 读入经营范围专用stop words, 并进行简单分词与过滤
print('读入经营范围专用stop words, 并进行简单分词与过滤')
with open('stop_words/business_stop_words.txt','r') as f:
    business_stop_words = f.read().splitlines()
all_business_labels = []
for sample in scope_str_list:
    business_labels = []
    sample_split = re.findall(r"[\w']+|[，。；、]", sample)
    for token in sample_split:
        if 2 < len(token) and len(token) < 100 and not any(w in token for w in business_stop_words):
            business_labels.append(token)
    all_business_labels.append(business_labels)

# 去除重复标签
labels_no_duplicate = []
for line in all_business_labels:
    tmp = list(dict.fromkeys(line))
    labels_no_duplicate.append(tmp)

# 存入数据库
print('存入数据库')
for i, labels in enumerate(labels_no_duplicate):
    cp.update_one({"_id":id_list[i]},{"$set":{"business_labels":labels}})

# simple tf-idf topic words extraction
# cut_docs = [jieba.lcut(doc) for doc in scope_str_list]
# cut_docs = [" ".join(cut_doc) for cut_doc in cut_docs]

# with open('zh_stop_words/general_stop_words.txt','r',encoding='utf-8') as f:
#     stop_words = (f.readlines())
# stop_words = [stop_word.strip('\n') for stop_word in stop_words]

# vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=stop_words)
# occur_mat = vectorizer.fit_transform(cut_docs)
# words = vectorizer.get_feature_names()

# transformer = TfidfTransformer()
# tfidf = transformer.fit_transform(occur_mat)
# weight = tfidf.toarray()

# top_k = 10
# for w in weight:
#     sorted_index = np.argsort(w)
#     for i in range(top_k):
#         print(words[sorted_index[i]], end=' ')
#     print()


# %%
