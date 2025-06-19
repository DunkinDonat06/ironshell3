import requests

def send_webhook(payload, url):
    resp = requests.post(url, json=payload)
    return resp.ok, resp.text