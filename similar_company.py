#%%
from src.mongo_utils import get_company_profile_collection
import pandas as pd
# %%
cp = get_company_profile_collection()
df = pd.DataFrame(list(cp.find({},{"_id":1, "businessScope":1})))
df = df.dropna()
scope_str_list = df['businessScope'].to_list()
id_list = df['_id'].to_list()
