from urllib.request import urlopen
from urllib.request import Request
import datetime
import json
import requests
import pandas as pd
import numpy as np


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization':'token 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', # need to give the token if we use github-api
        'Content-Type':'application/json',
        'method': 'GET',
        'Accept': 'application/json'
    }
    html = requests.get(url, headers=headers) # send request
    if html.status_code == 200: # if succeed
        # print(html)
        return html.content # return the content
    else:
        return None


# this function is used to get the top100 contributors from the repo
def get_repo_contributor(owner,repo):
    url_repos = 'https://api.github.com/repos/{owner}/{repo}/contributors?page=1&per_page=100'.format(owner=owner,repo=repo)
    html = get_data(url_repos)
    json_data = json.loads(html)
    all_contributor = []  #store contributors data
    for  i in range(len(json_data)):
        diction={}
        diction['name']=json_data[i]["login"]
        diction['contributions']=json_data[i]["contributions"]
        all_contributor.append(diction)

    print(json_data)
    print(all_contributor)
    return all_contributor

if __name__=='__main__':
    all_contributor=get_repo_contributor('tensorflow','tensorflow')
    contributor_event=[]
    for item in all_contributor:
        name=item['name']
        print(name)
        event = []
        # because github can only store 100 events in one page, we take 300 events(seems the maximum events are 300)
        for page in range(1,4):
            url='https://api.github.com/users/{name}/events?page={page}&per_page=100'.format(name=name,page=page)
            headers = {
                    'User-Agent': 'Mozilla/5.0',
                'Authorization':'token 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',
                'Content-Type':'application/json',
                'method': 'GET',
                    'Accept': 'application/json'
                }
            print(url)
            html = get_data(url) # send request
            json_data = json.loads(html)
            for item in json_data:
                temp={}
                temp['event']=item['type']
                temp['repo']=item['repo']
                # the common 8 events
                if item['type'] in ['PushEvent','CreateEvent','DeleteEvent','PullRequestEvent','CommitCommentEvent','IssueCommentEvent','PullRequestReviewCommentEvent',
                                       'IssuesEvent']:
                    event.append(temp)
        print(event)
        diction={}
        diction['name']=name
        diction['event']=event
        contributor_event.append(diction)

    print(contributor_event)

    # count the events for each contributor
    contributor_events = pd.DataFrame(columns=[
        ### Below are standard commit infomation
        'name',
        'Issue',
        'PullRequestReviewComment',
        'IssueComment',
        'CommitComment',
        'PullRequest',
        'Push',
        'Create/Delete',
    ])
    for item in contributor_event:
        Issue=0
        CommitComment=0
        Push=0
        Create_Delete=0
        IssueComment=0
        PullRequest=0
        PullRequestReview=0
        for event in item['event']:
            if event['event']=='IssuesEvent':
                Issue+=1
            if event['event']=='PushEvent':
                Push+=1
            if event['event'] == 'PullRequestEvent':
                PullRequest+=1
            if event['event']=='IssueCommentEvent':
                IssueComment+=1
            if event['event'] == 'PullRequestReviewCommentEvent':
                PullRequestReview+=1
            if event['event']=='CreateEvent' or event['event']=='DeleteEvent':
                Create_Delete+=1
            if event['event']=='CommitCommentEvent':
                CommitComment+=1
        contributor_events = contributor_events.append({
            'name':item['name'],
            'Issue':Issue,
            'PullRequestReviewComment': PullRequestReview,
            'IssueComment': IssueComment,
            'CommitComment': CommitComment,
            'PullRequest':PullRequest,
            'Push':Push,
            'Create/Delete':Create_Delete,

        }, ignore_index=True)

    # print(contributor_events.head(5))
    # print(contributor_events.iloc[1])
    # print(contributor_events['PullRequestReviewComment'].sum())
    # print(contributor_events['CommitComment'].sum())
    contributor_events.to_csv('./contributor_events.csv')