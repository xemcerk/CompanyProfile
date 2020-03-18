import pymongo
import pandas as pd

client = pymongo.MongoClient(host='10.108.210.101')
df = pd.DataFrame(list(client.TechBigData.CompanyProfile.find({},{"businessScope":1})))
scope_str_list = df['businessScope'].dropna().to_list()

import jieba
cut_docs = [jieba.lcut(doc) for doc in scope_str_list]
cut_docs = [" ".join(cut_doc) for cut_doc in cut_docs]

with open('zh_stop_words\\stop_words.txt','r',encoding='utf-8') as f:
    stop_words = (f.readlines())
stop_words = [stop_word.strip('\n') for stop_word in stop_words]

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=stop_words)
tf = tf_vectorizer.fit_transform(cut_docs)
tf_feature_names = tf_vectorizer.get_feature_names()

from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components=6, max_iter=100, random_state=42).fit(tf)
doc_topic = lda.transform(tf)

com_prfl = client.TechBigData.CompanyProfile
id_list = list(com_prfl.find({},{"_id":1}))
for i, vec in enumerate(doc_topic):
    com_prfl.update_one({"_id":id_list[i]['_id']},{"$set":{"topicVec":vec.tolist()}})





