# %%
import pymongo
#%%
def get_company_profile_collection():
    client = pymongo.MongoClient(host='49.234.215.201', serverSelectionTimeoutMS=5000)
    return client.TechBigData.CompanyProfile