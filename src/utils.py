import json
import time
import re
import sqlite3
import calendar
from datetime import datetime
from os import getcwd, path


prefixs = {}
with open("prefixs.json") as prf:
    prefixs = json.load(prf)


def as_timestamp(date):
    return int(time.mktime(datetime.fromisoformat(date).timetuple()))

def to_format(text):
    k = re.sub(r"(\[|\]|\s)", 
                lambda m : "_" if m.group(0) == " " else "", 
                text.group(0).lower())

    return prefixs[k] if k in prefixs.keys() else ""
    
def format_title(title: str):
    return re.sub(r"^\[(\w|\s)*\]", 
        to_format, 
        title)


def get_field_from_date(dt):
    fields = [
        {
            "name" : format_title(i[3]),
            "value" : f":arrow_forward: **Start** : <t:{as_timestamp(i[0])}>\n:pause_button: **End :** <t:{as_timestamp(i[1])}>\n:map: **Place** : `{i[2]}`\n:teacher: **With** : `{i[4]}`"
        } 
        for i in get_data_from_date(dt)
    ] 

    if(len(fields) <= 0): return {}

    return {
        "title" : f"{calendar.day_name[dt.date().weekday()].capitalize()} {str(dt.date())}",
        "fields" : fields
    }

def get_data_from_date(dt):
    connexion = sqlite3.connect(path.join(getcwd(), "./data/database.db"))
    data = connexion.execute("SELECT * FROM events WHERE DATE(start) = DATE(?)", [str(dt.date())]).fetchall()

    return data

def as_embed(data):
    return {
        "title" : "Next Event :",
        "color" : 0x2f3136,
        "fields" : [
                {
                "name" : format_title(data[3]),
                "value" : f":arrow_forward: **Start** : <t:{as_timestamp(data[0])}>\n:pause_button: **End :** <t:{as_timestamp(data[1])}>\n:map: **Place** : `{data[2]}`\n:teacher: **With** : `{data[4]}`"
            }
        ]
    }