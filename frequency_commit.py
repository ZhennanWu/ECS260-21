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

commit_email= []
for row in rows:
    commit_email.append(row[11])
frequency_email = pd.value_counts(commit_email)
frequency_email = frequency_email.reset_index().values.tolist();

frequency_email = np.asarray(frequency_email)
frequency_email = np.ndarray.tolist(frequency_email[:,1])
frequency_email = list(map(int,frequency_email))
print(frequency_email)
avg_commit = np.average(frequency_email)
print(avg_commit)
no_dev = range(1,len(frequency_email)+1)

plt.figure(1)
plt.bar(no_dev,frequency_email)
plt.axhline(avg_commit,color='gray')
plt.xlabel('Developers')
plt.ylabel('Number of Commits')
plt.text(no_dev[-1]-2,9,"Average: "+str(round(avg_commit,2)))


perc_freq_commit = frequency_email/avg_commit
plt.figure(2)
plt.bar(no_dev,perc_freq_commit)

plt.xlabel('Developers')
plt.ylabel('Number of Commits to Average')

plt.show();

