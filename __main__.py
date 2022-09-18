import json
import os
import threading

from src.utils.config import get_config
from src.utils.calendar import create_calendar


config = get_config()
create_calendar(config)