from pydriller import *
import pandas as pd
from datetime import date, datetime
from analyze import *
import numpy as np

url1="https://github.com/tensorflow/tensorflow.git"
url2="https://github.com/spring-projects/spring-boot.git"
url3='https://github.com/NVIDIA/DeepLearningExamples'
url4='D:/github_project/tensorflow/'
urls = [url4]
since = datetime(2019, 11, 10, 17, 0, 0)


def evaluate_value_doc(modified_file: ModifiedFile):
    return modified_file.added_lines * 0.01


######## Start commit data collection
commit_data = pd.DataFrame(columns=[
    ### Below are standard commit infomation
    'hash',
    'author',
    'author_email',
    'author_date',
    'lines',
    'dmm_score',
    ### Below are statistics from individual files
    'value',
    'added_lines_py',
    'deleted_lines_py',
])

for commit in Repository(path_to_repo=urls, since=since).traverse_commits():
    ### Each modified source file will produce a statistic
    print("commit {}, date {}".format(
        commit.hash, commit.author_date))
    print('dmm_size{},dmm_complexity{},dmm_interfacing{}'.format(commit.dmm_unit_size,
                commit.dmm_unit_complexity,
                commit.dmm_unit_interfacing))



    modified_src_stat = pd.DataFrame(columns=[
        'value',
        'added_lines_py',
        'deleted_lines_py'
    ])
    doc_value = 0
    for modified_file in commit.modified_files:
        if modified_file.filename.endswith((".py",".cc")):
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
    if commit.dmm_unit_size!=None and commit.dmm_unit_complexity!=None and commit.dmm_unit_interfacing!=None:
        dmm_score=commit.dmm_unit_size+commit.dmm_unit_complexity+ commit.dmm_unit_interfacing
    else:
        dmm_score=0
    print('dmm_score')
    print(dmm_score)

    commit_data = commit_data.append({
        'hash': commit.hash,
        'author':commit.author.name,
        'author_email': commit.author.email,
        'author_date': commit.author_date,
        'lines': commit.lines,
        'value': stat['value'] + doc_value,
        'added_lines_py': stat['added_lines_py'],
        'deleted_lines_py': stat['deleted_lines_py'],
        'dmm_score':dmm_score
    }, ignore_index=True)

    commit_data=commit_data.drop(commit_data[commit_data['dmm_score']==-1].index)


######## Usage of generated commit data
commit_data.to_csv('./commit_data.csv')
commit_data.groupby('author').aggregate(
    commit_count = ('hash', 'size'),
    lines = ('lines', 'sum'),
    value = ('value', 'sum'),
    dmm_score=('dmm_score','sum')
).to_csv('data.csv')