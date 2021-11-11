import numpy as np
import csv
import collection
import pandas as pd
import matplotlib.pyplot as plt

filename = "commit_data.csv"

fields = []
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)

    for row in csvreader:
        rows.append(row)
# print(type(rows))
df = pd.DataFrame(rows,columns=fields)
df['insertions'] = pd.to_numeric(df['insertions'])
df['deletions'] = pd.to_numeric(df['deletions'])
print(type(df['deletions'][1]))
ds = df.groupby(by='author').agg({'insertions':['sum'],'deletions':['sum']})
ds.reset_index()
ds['LOC_total'] = ds['insertions','sum'] + ds['deletions','sum']
print(ds)

no_dev = range(1,len(ds['LOC_total'])+1)
avg_pyLOC = np.average(ds['LOC_total'])
plt.figure(1)
plt.bar(no_dev,ds['LOC_total'])
plt.axhline(avg_pyLOC,color='gray')
plt.xlabel('Developers')
plt.ylabel('Lines of code')
plt.text(no_dev[-1]-2.5,avg_pyLOC,"Average: "+str(round(avg_pyLOC,2)))


plt.show()
