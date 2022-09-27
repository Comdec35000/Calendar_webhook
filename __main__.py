import requests
import schedule
import time
import sqlite3

from os import getcwd, path
from datetime import datetime, timedelta
from src.config import get_config
from src.calendar import create_calendar
from src.discord import send_weekly_url, send_daily_url, send
from src.utils import as_embed, get_field_from_date


def lifecycle(config):
    if config["webhook"].startswith("https://"): schedule.every().minutes.do(check_current, config=config)
    if config["webhook_daily"].startswith("https://"): schedule.every().days.at("00:00").do(check_daily, config=config)
    schedule.every().monday.at("00:00").do(check_for_week, config=config)

    while True:
        schedule.run_pending()
        time.sleep(1)


def check_current(config):
    if not config["webhook"].startswith("https://"): return

    connexion = sqlite3.connect(path.join(getcwd(), "./data/database.db"))
    data = connexion.execute("SELECT * FROM events WHERE DATETIME(start) < ?", [str((datetime.now()))]).fetchall()

    if len(data) == 0: return

    data = data.pop()
    send(config, as_embed(data))
    
    connexion.execute("DELETE FROM events WHERE date('now') >= end")
    connexion.commit()

def check_daily(config):
    if not config["webhook_daily"].startswith("https://"): return
    
    data = get_field_from_date(datetime.fromisoformat(str(datetime.today().date())))
    send_daily_url(config, data if len(data.keys()) > 0 else {"title": "Nothing to do today !"})

def check_for_week(config):

    send_weekly_url(config, {
            "title" : f"Emploi du temps de la semaine du {datetime.today().date()} au {(datetime.today() + timedelta(days=6)).date()}"
        })

    embeds = []
    for i in range(0, 7):
        embed = get_field_from_date(datetime.fromisoformat(str(datetime.today().date())) + timedelta(days=i))
        if len(embed.keys()) > 0 : 
            embed["color"] = 0x5865F2 
            embeds.append(embed)

    send_weekly_url(config, embeds)


if __name__ == "__main__" :
    config = get_config()
    create_calendar(config)

    print("Starting the application lifecycle...")
    lifecycle(config)