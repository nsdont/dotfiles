#!/usr/local/bin/python3

import sys
import click
import yaml
import requests
import uuid

from urllib.parse import urljoin
from os.path import expanduser

with open(expanduser('~/.config/person/jira2todoist.yaml')) as f:
    CONFIG = yaml.load(f.read())
    JIRA_ISSUE_URL = urljoin(CONFIG['JIRA_URL'], 'rest/api/2/issue/')


def req_todoist(method, url, payload):
    req_method = getattr(requests, method)
    return req_method(url, json=payload,
                      params={"token": CONFIG['TODOIST_TOKEN']},
                      headers={"X-Request-Id": str(uuid.uuid4())})


@click.command()
@click.argument('issue_id')
def main(issue_id):
    issue_url = urljoin(JIRA_ISSUE_URL, issue_id)
    headers = {
        "Authorization": CONFIG['JIRA_TOKEN'],
        "Content-Type": "application/json",
    }
    response = requests.get(issue_url, headers=headers)
    if (response.status_code != 200):
        print('get jira issues info failed, pleace check issue id.')
        sys.exit(-1)
    else:
        issue_data = response.json()
        issue_ref_url = urljoin(CONFIG['JIRA_URL'], '/browse/{}'.format(issue_id))

        todoist_payload = {
            "content": issue_data['fields']['summary'],
            "label_ids": [2148243744],
            "priority": 2,
            "project_id": 2156437167
        }
        task_response = req_todoist('post', urljoin(CONFIG['TODOIST_URL'], 'tasks'),
                                    todoist_payload)

        if (task_response.status_code == 200):
            print('create todoist task success.')
            comment_payload = {
                'task_id': task_response.json()['id'],
                'content': issue_ref_url,
            }
            req_todoist('post', urljoin(CONFIG['TODOIST_URL'], 'comments'),
                        comment_payload)
        else:
            print('create todoist task failed.')
            print(task_response.content)
            sys.exit(-2)

if __name__ == '__main__':
    main()
