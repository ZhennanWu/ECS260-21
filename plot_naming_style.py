import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller import *
from analysis.identifier_name import NamingStyle

from analyze import *

from datetime import date, datetime

repo_names = ['AWS Data Wrangler', 'PyMC', 'NumPy']

def deduce_lower_camel_or_snake(stat):
    deduced_stat = [count for count in stat]
    if stat[NamingStyle.LowerCamel.value] <= stat[NamingStyle.Snake.value]:
        deduced_stat[NamingStyle.Snake.value] += deduced_stat[NamingStyle.LowerCamelOrSnake.value]
    else:
        deduced_stat[NamingStyle.LowerCamel.value] += deduced_stat[NamingStyle.LowerCamelOrSnake.value]
    deduced_stat[NamingStyle.LowerCamelOrSnake.value] = 0
    return deduced_stat

def calc_freq(stat):
    all_count = max(1,sum(stat))
    freq = [count * 1.0/all_count for count in stat]
    freq.pop(NamingStyle.LowerCamelOrSnake.value)
    return freq


analyze_freq = np.vectorize(calc_freq)

for i in range(3):
    #this file give some figures about the contribution between the top contributors and median
    df_commit=pd.read_csv('./commit_data_{}.csv'.format(i))

    df_data=pd.read_csv('./data_{}.csv'.format(i))
    df_data['var_names_style_stat'] = df_data['var_names_style_stat'].apply(ast.literal_eval)
    df_data['fun_names_style_stat'] = df_data['fun_names_style_stat'].apply(ast.literal_eval)
    df_data['class_names_style_stat'] = df_data['class_names_style_stat'].apply(ast.literal_eval)

    df_data['var_names_style_stat_deduced'] = df_data['var_names_style_stat'].apply(deduce_lower_camel_or_snake)
    df_data['fun_names_style_stat_deduced'] = df_data['fun_names_style_stat'].apply(deduce_lower_camel_or_snake)
    df_data['class_names_style_stat_deduced'] = df_data['class_names_style_stat'].apply(deduce_lower_camel_or_snake)

    df_data['var_names_style_freq']= df_data['var_names_style_stat_deduced'].apply(calc_freq)
    df_data['fun_names_style_freq']= df_data['fun_names_style_stat_deduced'].apply(calc_freq)
    df_data['class_names_style_freq']= df_data['class_names_style_stat_deduced'].apply(calc_freq)

    df_data['scores']=df_data['commit_count']+df_data['lines']+df_data['dmm_score']

    df_data=df_data.sort_values(by=['scores'],ascending=[False])
    df_sum = df_data.groupby(lambda x: True).agg(
        commit_count=('commit_count', 'sum'),
        lines=('lines', 'sum'),
        **py_source_stat_combiner,
        var_names_style_stat_deduced=('var_names_style_stat_deduced', naming_style_sum),
        fun_names_style_stat_deduced=('fun_names_style_stat_deduced', naming_style_sum),
        class_names_style_stat_deduced=('class_names_style_stat_deduced', naming_style_sum),
    )
    df_sum['var_names_style_freq']= df_sum['var_names_style_stat_deduced'].apply(calc_freq)
    df_sum['fun_names_style_freq']= df_sum['fun_names_style_stat_deduced'].apply(calc_freq)
    df_sum['class_names_style_freq']= df_sum['class_names_style_stat_deduced'].apply(calc_freq)

    df_data['comment_to_code_ratio'] = df_data['added_comment'] / df_data['added_code_lines']
    df_data['pure_comment_lines'] = df_data['added_lines_py'] - df_data['added_code_lines']
    df_data['inline_comments'] = df_data['added_comment'] - df_data['pure_comment_lines']
    df_data['commented_code_ratio'] = df_data['inline_comments'] / df_data['added_code_lines']
    df_data['inline_commented_ratio'] = df_data['inline_comments'] / df_data['added_comment']

    df_sum['comment_to_code_ratio'] = df_sum['added_comment'] / df_sum['added_code_lines']
    df_sum['pure_comment_lines'] = df_sum['added_lines_py'] - df_sum['added_code_lines']
    df_sum['inline_comments'] = df_sum['added_comment'] - df_sum['pure_comment_lines']
    df_sum['commented_code_ratio'] = df_sum['inline_comments'] / df_sum['added_code_lines']
    df_sum['inline_commented_ratio'] = df_sum['inline_comments'] / df_sum['added_comment']

    df_data['fun_per_100_LOC'] = df_data['fun_names_style_stat'].apply(lambda x: sum(x)) * 1.0 / df_data['added_code_lines'].apply(lambda x: max(1,x)) * 100


    print(df_data.head(5))
    df_data.drop(index=[0],inplace=True)
    number_of_len=np.arange(len(df_data))
    top_10=int(np.percentile(number_of_len,10))
    mid_55=int(np.percentile(number_of_len,60))
    mid_45=int(np.percentile(number_of_len,40))
    print(top_10)
    print(mid_45)
    print(mid_55)
    # print(df_score(in_qrange, q=[0.1, 0.5]))
    top_10_contributor=df_data.iloc[:top_10]
    mid_contributor=df_data.iloc[mid_45:mid_55]

    top_10_contributor_filtered = top_10_contributor[top_10_contributor['var_names_style_stat'].apply(lambda x: sum(x)) > 50]
    top_10_contributor_filtered.to_csv('data_top_10_{}.csv'.format(i))

    mid_contributor_filtered = mid_contributor[mid_contributor['added_code_lines'] > 100]
    mid_contributor.to_csv('data_mid_10_{}.csv'.format(i))
    df_sum.to_csv('sum_{}.csv'.format(i))
    commits=[top_10_contributor['commit_count'],mid_contributor['commit_count']]

    naming_styles = ['Single Character', 'lowerCamelCase', 'UpperCamelCase', 'SCREAMING_SNAKE_CASE', 'snake_case', 'Upper_Snake_Case', 'uNKnowN']
    grouped_data = [[top_10_contributor_filtered['var_names_style_freq'].iloc[j][i] for j in range(top_10_contributor_filtered.shape[0])] for i in range(len(naming_styles))]
    fig, ax = plt.subplots()
    ax.set_ylim((0,1))
    ax.bar(range(1, len(naming_styles)+1), df_sum['var_names_style_freq'].iloc[0], color='yellow', align='center')
    ax2 = ax.twinx()
    ax2.boxplot(grouped_data)
    ax2.set_ylim(ax.get_ylim())
    for x in range(len(naming_styles)):
        ax2.plot(np.random.normal(1+x, 0.04, size=top_10_contributor_filtered.shape[0]), grouped_data[x], 'r.', alpha = 0.2)
    ax.set_xticklabels(naming_styles, rotation=45, ha='right')
    ax.set_title('Variable Naming Styles in {}'.format(repo_names[i]))
    fig.tight_layout()
    plt.show()


    selected_cols = ['comment_to_code_ratio', 'commented_code_ratio', 'inline_commented_ratio']
    x_labels = ['Comment lines/code lines', '% of code with inline comment', '% of inline comment']
    grouped_data = [[top_10_contributor[selected_cols[i]].iloc[j] for j in range(top_10_contributor.shape[0])] for i in range(len(selected_cols))]
    fig, ax = plt.subplots()
    ax.set_ylim((0,1))
    ax.bar(range(1, len(selected_cols)+1), df_sum[selected_cols].iloc[0], color='yellow', align='center')
    ax2 = ax.twinx()
    ax2.boxplot(grouped_data)
    ax2.set_ylim(ax.get_ylim())
    for x in range(len(selected_cols)):
        ax2.plot(np.random.normal(1+x, 0.04, size=top_10_contributor.shape[0]), grouped_data[x], 'r.', alpha = 0.2)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_title('Comment Behaviors in {}'.format(repo_names[i]))
    fig.tight_layout()
    plt.show()

    x_labels = ['Top contributors', 'Average contributors']
    fig, ax = plt.subplots()
    # ax.set_ylim((0,1))
    ax.boxplot([top_10_contributor['fun_per_100_LOC'], mid_contributor_filtered['fun_per_100_LOC']])
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.plot(np.random.normal(1, 0.04, size=top_10_contributor.shape[0]), top_10_contributor['fun_per_100_LOC'], 'r.', alpha = 0.2)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_title('Functions & Methods Per 100 SLOC in {}'.format(repo_names[i]))
    fig.tight_layout()
    plt.show()

    



    



