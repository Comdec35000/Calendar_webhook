from dataclasses import fields
import json
import time
import re
import sqlite3
import requests
from os import getcwd, path
from datetime import datetime, timedelta


prefixs = {}
with open("prefixs.json") as prf:
    prefixs = json.load(prf)

def url(config): 
    return config["webhook"]

def check_current(config):
    now = str((datetime.now() + timedelta(hours=-6)))
    print(now)

    connexion = sqlite3.connect(path.join(getcwd(), "./data/database.db"))
    data = connexion.execute("SELECT * FROM events WHERE DATETIME(start) < ?", [now]).fetchall()

    if len(data) == 0: 
        print("no event")
        return

    data = data.pop()
    send_embed(config, {
        "title" : "Next Event :",
        "color" : 0x2f3136,
        "fields" : [
                {
                "name" : format_title(data[3]),
                "value" : f":arrow_forward: **Start** : <t:{as_timestamp(data[0])}>\n:pause_button: **End :** <t:{as_timestamp(data[1])}>\n:map: **Place** : `{data[2]}`\n:teacher: **With** : `{data[4]}`"
            }
        ]
    })
    
    connexion.execute("DELETE FROM events WHERE date('now') >= end")
    connexion.commit()

def check_daily(config):
    send_embed(config, send_for_date(config, datetime.fromisoformat(str(datetime.today().date()))))

def check_for_week(config):
    send_embed(config, {
            "title" : f"Emploi du temps de la semaine du {datetime.today().date()} au {(datetime.today() + timedelta(days=6)).date()}"
        })


    embeds = []
    for i in range(0, 7):
        embed = send_for_date(config, datetime.fromisoformat(str(datetime.today().date())) + timedelta(days=i))
        if len(embed.keys()) > 0 : 
            embed["color"] = 0x5865F2 
            embeds.append(embed)

    requests.post(url(config), json = {
        "username" : "Calendar",
        "embeds" : embeds
    })

def send_for_date(config, dt):
    connexion = sqlite3.connect(path.join(getcwd(), "./data/database.db"))
    data = connexion.execute("SELECT * FROM events WHERE DATE(start) = DATE(?)", [str(dt.date())]).fetchall()

    fields = [
        {
            "name" : format_title(i[3]),
            "value" : f":arrow_forward: **Start** : <t:{as_timestamp(i[0])}>\n:pause_button: **End :** <t:{as_timestamp(i[1])}>\n:map: **Place** : `{i[2]}`\n:teacher: **With** : `{i[4]}`"
        } 
        for i in data
    ] 

    if(len(fields) <= 0): return {}

    return {
        "title" : str(dt.date()),
        "fields" : fields
    }

def send_embed(config, payload):
    r = requests.post(url(config), json = {
        "username" : "Calendar",
        "embeds" : [payload]
    })

def as_timestamp(date):
    return int(time.mktime(datetime.fromisoformat(date).timetuple()))

def format_title(title: str):
    return re.sub(r"^\[(\w|\s)*\]", 
        lambda match: prefixs[
            re.sub(r"(\[|\]|\s)", 
                lambda m : "_" if m.group(0) == " " else "", 
                match.group(0).lower())
            ] if re.sub(r"(\[|\]|\s)", 
                lambda m : "_" if m.group(0) == " " else "", 
                match.group(0).lower()) in prefixs.keys() else "", 
        title)