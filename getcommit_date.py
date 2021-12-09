from urllib.request import urlopen
from urllib.request import Request
import datetime
import json
import requests
import pandas as pd
import numpy as np
from getrepo import get_data, get_repo_contributor
import re
import time
import os

def get_html(url):
    user_agent = 'Mozilla/5.0'
    try:
        headers = {'User-Agent': user_agent}
        html = requests.get(url, headers=headers)
        # print("html status code is",html.status_code)
        if html.status_code == 200: # 判断请求是否成功
            # print(html)
            return html.text # 返回网页内容
    except Exception as e:
        print ('Wrong!!!',e)


def get_sha(user, repo_name): # 用户的每个repo对应一个commit sha
    url = "https://github.com/{user}/{repo_name}/commits/master".format(user=user, repo_name=repo_name)
    html = get_html(url)
    commit_sha=0
    if html==None:
        commit_sha=0
    else:
        commit_sha = re.findall(r'href="https://github.com/.*commit/(.*?)"', html)[0]
    print(commit_sha)
    return commit_sha

def single_repo_commits(user, repo_name):
    num = 0
    page_flag = 66 # 设置页面初始标志,用于判断是否到达末页
    page_num = 0
    data_num = 0
    commit_sha = get_sha(user, repo_name)
    if commit_sha!=0:
        all_date = [] # 储存时间数据

        while (page_flag and page_num<5): # 测试前五页
            url = "https://github.com/{user}/{repo_name}/commits/master?after={commit_sha}+{num}".format(user=user, repo_name=repo_name, commit_sha=commit_sha, num=num) # 构建链接
            html = get_html(url) # 获取页面内容
            time_data = re.findall(r'<relative-time datetime=(.*)</relative-time>', html) # re匹配时间元素
            page_flag = len(time_data)
            num = num + 34 # 进入下一页
            page_num = page_num+1
            data_num = data_num+len(time_data)
            print("page %d is ok\n get %d date" % (page_num, len(time_data)))
            for date in time_data:
                all_date.append(date[1:20])
            time.sleep(1)
        print("the repo <%s> totally get %d commits'date" % (repo_name, data_num))
        return all_date
    else:
        all_date=None
        return all_date

if __name__=='__main__':
    all_contributor=get_repo_contributor('tensorflow','tensorflow')
    print(all_contributor)
    for user in all_contributor:
        print(user['name'])
        all_date=single_repo_commits(user['name'], 'tensorflow')
        print(all_date)
