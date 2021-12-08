import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller import *

from datetime import date, datetime
#this file give some figures about the contribution between the top contributors and median
df_commit=pd.read_csv('./ECS260-21/commit_data.csv')

df_data=pd.read_csv('./ECS260-21/data.csv')
url="https://github.com/tensorflow/tensorflow.git"

df_score=pd.read_csv('scores.csv')
print(df_score.head(5))
first_author=df_score.iloc[1]['author']
length=len(df_score)
medium=int(length/2)
print(first_author)
print(medium)
medium_author=df_score.iloc[10]['author']
print(medium_author)
print(df_commit.head(5))
# df_commit.reset_index(inplace=True)
print(df_commit)
print(df_commit.columns)
df_commit.drop(columns=['Unnamed: 0'],axis=1,inplace=True)
df_commit['author_date']=pd.to_datetime(df_commit['author_date'], format='%Y/%m/%d', errors='ignore')
df_origin=df_commit.copy()
df_commit['author_date']=df_commit['author_date'].apply(lambda x: datetime.strftime(x, format='%Y-%m'))

df_month_plot=df_commit[df_commit['author']==first_author]
df_month_plot=df_month_plot.groupby(['author_date']).aggregate ( commit_count = ('hash', 'size'),
    lines = ('lines', 'sum'),
    value = ('value', 'sum'),
    dmm_score=('dmm_score',sum) )

df_medium=df_commit[df_commit['author']==medium_author]
df_medium=df_medium.groupby(['author_date']).aggregate ( commit_count = ('hash', 'size'),
    lines = ('lines', 'sum'),
    value = ('value', 'sum'),
    dmm_score=('dmm_score',sum) )
# df_month_plot.drop(df_month_plot.index[0],axis=0,inplace=True)

print(df_month_plot.index)
print(df_month_plot)
print(df_medium)

# plt.figure(figsize=(20,14))
# ax1=plt.subplot(221)
plt.bar(df_month_plot.index,df_month_plot['commit_count'],label='top contributor')
plt.bar(df_medium.index,df_medium['commit_count'],label='medium contributor')
plt.ylabel('commit_counts')
plt.legend()
plt.show()
# ax2=plt.subplot(222)
plt.bar(df_month_plot.index,df_month_plot['lines'].apply(lambda x: math.log(x)),label='top contributor')
plt.bar(df_medium.index,np.log(df_medium['lines']),label='medium contributor')
plt.ylabel('log lines')
plt.legend()
plt.show()
# ax2=plt.subplot(223)
plt.bar(df_month_plot.index,df_month_plot['dmm_score'],label='top contributor')
plt.bar(df_medium.index,df_medium['dmm_score'],label='medium contributor')
plt.ylabel('dmm_score')
plt.legend()
plt.show()

# df_origin['author_date']=df_origin['author_date'].apply(lambda x: datetime.strftime(x, format='%Y-%m-%d'))
# print(type(df_origin['author_date'][0]))

# print(new_data)
# print(df_commit['author_date'])
# authorlist=df_commit['author'].unique()
# print(authorlist)
# print(type(df_commit['author_date'][0]))
# new_data=df_commit.groupby(['author','author_date']).aggregate ( commit_count = ('hash', 'size'),
#     lines = ('lines', 'sum'),
#     value = ('value', 'sum'),)
# print(new_data)
#
# # print(new_data.iloc[0])
# for key ,value in new_data:
#     print('key')
#     print(key)
#     print('value')
#     print(value)
