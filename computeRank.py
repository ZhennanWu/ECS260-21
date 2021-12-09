import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller import *
# this file is to compute the contribution for each contributors, but not really rational

df_author=pd.read_csv('./ECS260-21/data.csv')
df_commit=pd.read_csv('./ECS260-21/commit_data.csv')

print(df_author.head(5))
print(df_author.columns)
columns=['commit_count', 'lines', 'dmm_score']
for column in columns:
    print(column)
    df_author[column]=df_author[column].astype(float)
    df_author[column]=df_author[column].apply(lambda x : (x)/(np.max(df_author[column]))*100)

print(df_author['commit_count'])
print(df_author['lines'])
print(df_author['dmm_score'])
df_author['scores']=df_author['commit_count']+df_author['lines']+df_author['dmm_score']
print(df_author['scores'])

# sort by the scores
df_author=df_author.sort_values(by=['scores'],ascending=[False])
df_author.to_csv('scores1.csv')