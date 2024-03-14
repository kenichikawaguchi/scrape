import json
from company import Company
import pandas as pd

from pprint import pprint

index_df = pd.read_csv("index_list.csv", delimiter='|')
with open('dump.json', 'r') as f:
    json_data = json.load(f)

pprint(json_data)

df = pd.json_normalize(json_data)
print(df)
print(index_df)
frame = [index_df, df]
print(frame)


