import requests
import os

def send_slack_notification(message, webhook_url=None):
    webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL не задан")
    resp = requests.post(webhook_url, json={"text": message})
    return resp.ok

def send_telegram_notification(message, bot_token=None, chat_id=None):
    bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not (bot_token and chat_id):
        raise ValueError("TELEGRAM_BOT_TOKEN и/или TELEGRAM_CHAT_ID не заданы")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    resp = requests.post(url, data=data)
    return resp.ok