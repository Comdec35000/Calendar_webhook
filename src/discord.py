from datetime import datetime
import requests
from datetime import datetime


def send_weekly_url(config, payload):
    send_embed(config["webhook_weekly"], payload)

def send_daily_url(config, payload):
    print(type(payload))
    send_embed(config["webhook_daily"], [dict(payload)])

def send(config, payload):
    print(type(payload))
    send_embed(config["webhook"], [dict(payload)])

def send_embed(url, payload):
    r = requests.post(url, json = {
        "username" : "Calendar",
        "embeds" : payload
    })

    print(f"[{str(datetime.now().date())}] Sended an embed to the url {url}, recived status code {r.status_code}")
