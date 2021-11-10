from pydriller import *
import pandas as pd
from datetime import date, datetime
from analyze import *
import numpy as np

urls = ["https://github.com/ishepard/pydriller.git"]
since = datetime(2020, 10, 8, 17, 0, 0)


def evaluate_value_doc(modified_file: ModifiedFile):
    return modified_file.added_lines * 0.01


######## Start commit data collection
commit_data = pd.DataFrame(columns=[
    ### Below are standard commit infomation
    'hash',
    'author_email',
    'author_date',
    'insertions',
    'deletions',
    'lines',
    ### Below are statistics from individual files
    'value',
    'added_lines_py',
    'deleted_lines_py',
])

for commit in Repository(path_to_repo=urls, since=since).traverse_commits():
    ### Each modified source file will produce a statistic
    modified_src_stat = pd.DataFrame(columns=[
        'value',
        'added_lines_py',
        'deleted_lines_py'
    ])
    doc_value = 0
    for modified_file in commit.modified_files:
        if modified_file.filename.endswith(".py"):
            modified_src_stat = modified_src_stat.append(analyze_src(modified_file), ignore_index=True)
        if modified_file.filename.endswith((".md", "adoc")): # TODO: more doc file types
            doc_value += evaluate_value_doc(modified_file)

    ### Combine the statistics from each individual source file
    stat = modified_src_stat.groupby(lambda x: True).aggregate(
        value=('value', 'sum'),
        added_lines_py=('added_lines_py', 'sum'),
        deleted_lines_py=('deleted_lines_py', 'sum'),
    ).to_dict('records')

    stat = stat[0] if len(stat) > 0 else {
        'value': 0,
        'added_lines_py': 0,
        'deleted_lines_py': 0,
    }

    commit_data = commit_data.append({
        'hash': commit.hash,
        'author': commit.author.email,
        'author_date': commit.author_date,
        'insertions': commit.insertions,
        'deletions': commit.deletions,
        'lines': commit.lines,
        'value': stat['value'] + doc_value,
        'added_lines_py': stat['added_lines_py'],
        'deleted_lines_py': stat['deleted_lines_py'],
    }, ignore_index=True)


######## Usage of generated commit data
commit_data.to_csv('commit_data.csv')
commit_data.groupby('author').aggregate(
    commit_count = ('hash', 'size'),
    lines = ('lines', 'sum'),
    value = ('value', 'sum')
).to_csv('data.csv')