import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller import *

from datetime import date, datetime

#this file give some figures about the contribution between the top contributors and median
df_commit=pd.read_csv('./commit_data-tensor.csv')

df_data=pd.read_csv('./data-tensor.csv')
# url="https://github.com/tensorflow/tensorflow.git"

df_score=pd.read_csv('scores-tensor.csv')
print(df_score.head(5))
df_score.drop(index=[0],inplace=True)
print(df_score.head(5))
number_of_len=np.arange(len(df_score))
top_10=int(np.percentile(number_of_len,20))
mid_55=int(np.percentile(number_of_len,60))
mid_45=int(np.percentile(number_of_len,40))
print(top_10)
print(mid_45)
print(mid_55)
print(np.arange(len(df_score)))
# print(df_score(in_qrange, q=[0.1, 0.5]))
top_10_contributor=df_score.iloc[:top_10]
mid_contributor=df_score.iloc[mid_45:mid_55]
commits=[np.log(top_10_contributor['commit_count']),np.log(mid_contributor['commit_count'])]
lines=[np.log(top_10_contributor['lines']),np.log(mid_contributor['lines'])]
dmm_score=[np.log(top_10_contributor['dmm_score']),np.log(mid_contributor['dmm_score'])]
scores=[np.log(top_10_contributor['scores']),np.log(mid_contributor['scores'])]
plt.figure(figsize=(10,8))
ax = plt.subplot(221)
plt.boxplot(commits,labels=['top contributor','mid contributor'])
plt.ylabel('log of commits')
# plt.show()
ax = plt.subplot(222)
plt.boxplot(lines,labels=['top contributor','mid contributor'])
plt.ylabel('log of LOC')
# plt.show()
ax = plt.subplot(223)
plt.ylabel('log of DMM score')
plt.boxplot(dmm_score,labels=['top contributor','mid contributor'])
# plt.show()
ax = plt.subplot(224)
plt.boxplot(scores,labels=['top contributor','mid contributor'])
plt.ylabel('log of total score')
plt.show()



# print(df_commit.head(5))
# # df_commit.reset_index(inplace=True)
# print(df_commit)
# print(df_commit.columns)
# df_commit.drop(columns=['Unnamed: 0'],axis=1,inplace=True)
# df_commit['author_date']=pd.to_datetime(df_commit['author_date'], format='%Y/%m/%d', errors='ignore')
# df_origin=df_commit.copy()
# df_commit['author_date']=df_commit['author_date'].apply(lambda x: datetime.strftime(x, format='%Y-%m'))
#
# df_month_plot=df_commit[df_commit['author']==first_author]
# df_month_plot=df_month_plot.groupby(['author_date']).aggregate ( commit_count = ('hash', 'size'),
#     lines = ('lines', 'sum'),
#     value = ('value', 'sum'),
#     dmm_score=('dmm_score',sum) )
#
# df_medium=df_commit[df_commit['author']==medium_author]
# df_medium=df_medium.groupby(['author_date']).aggregate ( commit_count = ('hash', 'size'),
#     lines = ('lines', 'sum'),
#     value = ('value', 'sum'),
#     dmm_score=('dmm_score',sum) )
# # df_month_plot.drop(df_month_plot.index[0],axis=0,inplace=True)
#
# print(df_month_plot.index)
# print(df_month_plot)
# print(df_medium)
#
# # plt.figure(figsize=(20,14))
# # ax1=plt.subplot(221)
# plt.bar(df_month_plot.index,df_month_plot['commit_count'],label='top contributor')
# plt.bar(df_medium.index,df_medium['commit_count'],label='medium contributor')
# plt.ylabel('commit_counts')
# plt.legend()
# plt.show()
# # ax2=plt.subplot(222)
# plt.bar(df_month_plot.index,df_month_plot['lines'].apply(lambda x: math.log(x)),label='top contributor')
# plt.bar(df_medium.index,np.log(df_medium['lines']),label='medium contributor')
# plt.ylabel('log lines')
# plt.legend()
# plt.show()
# # ax2=plt.subplot(223)
# plt.bar(df_month_plot.index,df_month_plot['dmm_score'],label='top contributor')
# plt.bar(df_medium.index,df_medium['dmm_score'],label='medium contributor')
# plt.ylabel('dmm_score')
# plt.legend()
# plt.show()
#
# # df_origin['author_date']=df_origin['author_date'].apply(lambda x: datetime.strftime(x, format='%Y-%m-%d'))
# # print(type(df_origin['author_date'][0]))
#
# # print(new_data)
# # print(df_commit['author_date'])
# # authorlist=df_commit['author'].unique()
# # print(authorlist)
# # print(type(df_commit['author_date'][0]))
# # new_data=df_commit.groupby(['author','author_date']).aggregate ( commit_count = ('hash', 'size'),
# #     lines = ('lines', 'sum'),
# #     value = ('value', 'sum'),)
# # print(new_data)
# #
# # # print(new_data.iloc[0])
# # for key ,value in new_data:
# #     print('key')
# #     print(key)
# #     print('value')
# #     print(value)
