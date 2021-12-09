import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns


# # we can choose some representative persons to see the events distribution
# df_plot=pd.read_csv('./contributor_events.csv')
# names=["*yong*","*mi*","*joker*"]
# print(df_plot.head(5))
# data=[df_plot.iloc[1],df_plot.iloc[6],df_plot.iloc[25]]
# df_plt=pd.DataFrame(data,index=names).drop(['Unnamed: 0'],axis=1)
# print(df_plt)
# df_plt.plot(kind="bar",stacked=True,figsize=(10,8))
# pl.xticks(rotation=360)
# plt.legend()
# plt.show()


df_rader=pd.read_csv('./contributor_events_radar.csv')
df_data=df_rader.iloc[50]
labels = np.array(['Coding','Comment','Issue'])
stats_1 = [df_data['target_code'],df_data['target_comment'],df_data['target_issue']]
print(stats_1)
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
print(angles)
stats = np.concatenate((stats_1, [stats_1[0]]))
angles = np.concatenate((angles, [angles[0]]))

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, stats, 'o-', linewidth=2)
ax.fill(angles, stats, alpha=0.25)

# 设置中文字体
# font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
ax.set_thetagrids(angles * 180/np.pi, labels)
plt.show()