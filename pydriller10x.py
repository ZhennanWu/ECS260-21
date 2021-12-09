from pydriller import *
import numpy as np
import pandas as pd
from datetime import date, datetime
from analyze import *
from analysis.identifier_name import NamingStyle

urls = ["https://github.com/ishepard/pydriller.git"]
# urls = ["../pydriller"]
since = datetime(2021, 5, 8, 17, 0, 0)
to = datetime.now()


def evaluate_value_doc(modified_file: ModifiedFile):
    return modified_file.added_lines * 0.01


# Start commit data collection


commit_dicts = []

for commit in Repository(path_to_repo=urls, since=since, to=to).traverse_commits():
    # Each modified source file will produce a statistic
    doc_value = 0
    per_source_file_stats = []
    for modified_file in commit.modified_files:
        if modified_file.filename.endswith(".py"):
            per_source_file_stats.append(analyze_src(modified_file))
        # TODO: more doc file types
        if modified_file.filename.endswith((".md", "adoc")):
            doc_value += evaluate_value_doc(modified_file)
    modified_src_stat = pd.DataFrame(per_source_file_stats, columns=py_source_stat_columns)

    # Combine the statistics from each individual source file
    stat = modified_src_stat.groupby(lambda x: True).aggregate(
        **py_source_stat_combiner
    ).to_dict('records')

    stat = stat[0] if len(stat) > 0 else py_source_stat_default

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


# Usage of generated commit data
commit_data.to_csv('commit_data.csv')
data_grouped_by_author = commit_data.groupby('author').aggregate(
    commit_count=('hash', 'size'),
    lines=('lines', 'sum'),
    **py_source_stat_combiner
)
data_grouped_by_author.to_csv('data.csv')
print(data_grouped_by_author['var_names_style_stat']['spadini.davide@gmail.com'][NamingStyle.Snake.value])