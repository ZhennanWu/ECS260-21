# For graders
The plot generating scripts are in `plot_naming_style.py`, `usepydriller.py`, `plot_event.py`, `frequency_commit.py`. The csv files are essential, as a fresh run of data collection usually takes more than 1 hour. A fresh run starts from pydriller10x.py and then `computeRank.py`.




# Previous notes during development
- The main logic is in pydriller10x.ipynb. It's a Jupyter Notebook
- The data is gathered from two sources: commit metadata, and each modified file in each commit



What you can do on top of this code:
1. You can copy-paste the main logic in pydriller10.py to get a function of `since` and `to`, so that you can analyze developer activities across time (e.g. weekly)
2. You can delete columns to free up memory usage. You should delete at these places
```
    commit_dicts.append({
        'hash': commit.hash,
        'author': commit.author.email,
        'author_date': commit.author_date,
        'insertions': commit.insertions,
        'deletions': commit.deletions,
        'lines': commit.lines,
        **stat,
        'value': stat['value'] + doc_value,
    })
```
and
```
commit_data = pd.DataFrame(commit_dicts, columns=[
    # Below are standard commit infomation
    'hash',
    'author',
    'author_date',
    'insertions',
    'deletions',
    'lines',
    # Below are statistics from individual files
    *py_source_stat_columns,
])
```
3. You can customize the value calculation method in analyzer.py (Line 47)
```
        'value': modified_src_file.added_lines * 0.1 + modified_src_file.deleted_lines * 0.01,
```
4. The naming styles is stored as a list
```
    'var_names_style_stat',
    'fun_names_style_stat',
    'class_names_style_stat',
```
You can access it by 
```
data_grouped_by_author['var_names_style_stat']['abc'][NamingStyle.Snake]
```