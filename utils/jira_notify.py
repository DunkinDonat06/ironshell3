import requests
import os

def send_jira_issue(summary, description, project_key, jira_url=None, user=None, token=None):
    jira_url = jira_url or os.environ.get("JIRA_URL")
    user = user or os.environ.get("JIRA_USER")
    token = token or os.environ.get("JIRA_TOKEN")
    url = f"{jira_url}/rest/api/2/issue"
    headers = {"Content-Type": "application/json"}
    auth = (user, token)
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"}
        }
    }
    resp = requests.post(url, json=payload, headers=headers, auth=auth)
    return resp.ok, resp.text