import requests
import schedule
import time

from src.config import get_config
from src.calendar import create_calendar
from src.discord import check_current, check_for_week, url


def lifecycle(config):
    schedule.every().minutes.do(check_current, config=config)
    schedule.every().days.at("00:00").do(check_for_week, config=config)
    schedule.every().monday.at("00:00").do(check_for_week, config=config)
    schedule.every().seconds.do(lambda: print("aaaa"))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__" :
    config = get_config()
    create_calendar(config)

    """payload = {
        "username" : "placeholder",
        "embeds" : [{"title" : "Application restarted !"}]
    }
    requests.post(url(config), payload)"""

    print("Starting the application lifecycle...")
    lifecycle(config)
    #thread = threading.Thread(target=lifecycle, args=(config,), name="lifecycle")
    #thread.start()