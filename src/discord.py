import sqlite3
import requests
from os import getcwd, path
from datetime import datetime, timedelta
from time import daylight


def check_current(config):
    print("aaa")

def check_daily(config):
    send_for_date(config, datetime.fromisoformat(str(datetime.today().date())))

def check_for_week(config):
    for i in range(0, 7):
        print(i)
        send_for_date(config, datetime.fromisoformat(str(datetime.today().date())) + timedelta(days=i))

def url(config): 
    return f"https://discord.com/api/webhooks/{config.get('id')}/{config.get('token')}"

def send_for_date(config, dt):
    connexion = sqlite3.connect(path.join(getcwd(), "./data/database.db"))
    data = connexion.execute("SELECT * FROM events WHERE DATE(start) = DATE(?)", [str(dt.date())]).fetchall()

    for i in data: print(i)
    #payload = {}

    #requests.post(url(config), payload)