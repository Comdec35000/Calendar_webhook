from datetime import datetime
from os import path, getcwd, remove, mkdir
from urllib import request
from requests import get
from icalendar import Calendar
import sys
import sqlite3


cal_path = path.join(getcwd(), "./assets/calendar_cache.ics")
db_path = path.join(getcwd(), "./data/database.db")


def create_calendar(config):
    if not check_calendar(config): 
        print("The Calendar have not been downloaded yet !")
        print("Downloading the calendar...")
        download(config["url"])
        print("Successfully downloaded the calendar !")
        print("Saving the calendar as a database...")
        ics_as_database()
        print("Successfully loaded the database")
    else:
        print("Calendar already downloaded !")
        print("Updating the database...")
        update_database()
        print("Database Updated !")


def check_calendar(config):
    if not path.exists(cal_path): return False
    if not path.exists(db_path): return False
    if config["url"] != config["url_old"]: return False
    with open(cal_path, "r", encoding="utf-8") as file:
        if len(file.readline()) <= 0: return False
    
    return True
    

def download(url):

    with open(cal_path, "wb") as f:
        response = get(url, stream=True)
        total_length = response.headers.get('content-length')

        # Displays a loading bar if the total length is too long
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()


def ics_as_database():

    if path.exists(db_path): remove(db_path)
    if not path.exists(path.join(getcwd(), "./data/")): mkdir(path.join(getcwd(), "./data/"))
    connexion = sqlite3.connect(db_path)

    connexion.execute("CREATE TABLE IF NOT EXISTS events (start TIMESTAMP, end TIMESTAMP, place VARCHAR(255), title VARCHAR(255), desc VARCHAR(1024));")

    today = datetime.today().date()

    with open(cal_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())
        events = [
            (
                comp.get("dtstart").dt,
                comp.get("dtend").dt,
                str(comp.get("location")[0]),
                str(comp.get("summary")),
                str(comp.get("description")),
            )
            for comp in calendar.walk() if comp.name == "VEVENT" and comp.get('dtstart').dt.date() >= today
        ]
        connexion.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?)", events)
        connexion.commit()
    
    connexion.close()


def update_database():
    connexion = sqlite3.connect(db_path)
    connexion.execute("DELETE FROM events WHERE date('now') >= end")