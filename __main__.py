import requests
import schedule
import time

from src.config import get_config
from src.calendar import create_calendar
from src.discord import check_current, check_for_week, url


def lifecycle(config):
    schedule.every(5).seconds.do(check_current, args=config)
    schedule.every().sunday.at("00:00").do(check_for_week, args=config)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__" :
    config = get_config()
    create_calendar(config)

    payload = {
        "username" : "placeholder",
        "embeds" : [{"title" : "Application restarted !"}]
    }
    requests.post(url(config), payload)

    print("Starting the application lifecycle...")
    lifecycle(config)
    #thread = threading.Thread(target=lifecycle, args=(config,), name="lifecycle")
    #thread.start()