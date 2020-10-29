#%%
import torch
import pymongo
import pandas as pd
import numpy as np 
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from transformers import BertTokenizer, BertModel
import matplotlib.pyplot as plt
#%%
# 从数据库读取数据
def get_company_profile_collection():
    client = pymongo.MongoClient(host='49.234.215.201',port=32919)
    return client.TechBigData.CompanyProfile
cp = get_company_profile_collection()
df = pd.DataFrame(list(cp.find({},{"_id":1, "business_labels":1})))
#%% 
# 去除空值
business_labels = df['business_labels'].dropna().to_list()
business_labels_rm_nan = []
for x in business_labels:
    if len(x)>0:
        business_labels_rm_nan.append(x)

#%%
# 去除重复值
all_labels = [x for labels in business_labels_rm_nan for x in labels]
all_labels_no_dup = {}
for x in all_labels:
    all_labels_no_dup[x] = 1
all_labels_no_dup_list = list(all_labels_no_dup.keys())
#%%
# 构建索引器
label2id = {}
for i, x in enumerate(all_labels_no_dup_list):
    label2id[x] = i
id2label = all_labels_no_dup_list
# %%
# 利用BERT进行文本编码
print("*************** Loading tokenizer ***************")
tokenizer = BertTokenizer.from_pretrained("hfl/chinese-bert-wwm")
print("*************** Loading BERT model ***************")
model = BertModel.from_pretrained("hfl/chinese-bert-wwm")
model.eval()
print("*************** Tokenizing labels ***************")
inputs = tokenizer(all_labels_no_dup_list, return_tensors='pt', padding=True)
print("*************** Encoding labels ***************")
with torch.no_grad():
    outputs = model(**inputs)
encoded_labels = outputs[1]
encoded_labels = encoded_labels.detach().cpu().numpy()
# %%
# 利用KMeans算法进行聚类分析
# print("*************** Use T-SNE to embedd encoded labels ***************")
# encoded_labels = TSNE(n_components=3).fit_transform(encoded_labels)
print("*************** Use KMeans to cluster labels ***************")
n_clusters = 100
kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(encoded_labels)
cluster_labels = kmeans.labels_
cluster2ids = {}
for i in range(n_clusters):
    cluster2ids[i] = []
for i, cluster in enumerate(cluster_labels):
    cluster2ids[cluster].append(i)

#%%
# 展示各个cluster中的标签
cluster = 17
for i in cluster2ids[cluster]:
    print(id2label[i])

#%%
# 5 设备制造
# 8 计算机相关
# 12 电信业务
# 13 百货
# %%
# 利用t-sne对标签进行可视化分析
labels_embedded = TSNE(n_components=3).fit_transform(encoded_labels)
fig, ax = plt.subplots()
ax.scatter(labels_embedded[:, 0], labels_embedded[: ,1], )

# %%
