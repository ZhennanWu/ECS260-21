import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns


# we can choose some representative persons to see the events distribution
df_plot=pd.read_csv('./contributor_events.csv')
names=["*yong*","*mi*","*joker*"]
print(df_plot.head(5))
data=[df_plot.iloc[1],df_plot.iloc[6],df_plot.iloc[25]]
df_plt=pd.DataFrame(data,index=names).drop(['Unnamed: 0'],axis=1)
print(df_plt)
df_plt.plot(kind="bar",stacked=True,figsize=(10,8))
pl.xticks(rotation=360)
plt.legend()
plt.show()