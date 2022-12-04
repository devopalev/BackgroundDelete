import json
import logging
import os
import threading
import time

import config


logger = logging.getLogger(__name__)


class LimiterHandlerPhoto:
    def __init__(self):
        self._lock = threading.Lock()
        self._last_photos = [0.0 for _ in range(config.COUNT_LIMIT_HANDLER_PHOTO)]

    def check(self):
        with self._lock:
            return (self._last_photos[0] - time.time()) < config.TIME_LIMIT_HANDLER_PHOTO

    def sent(self):
        with self._lock:
            self._last_photos.pop(0)
            self._last_photos.append(time.time())


class User:
    def __init__(self):
        self.limiter_send_photo = LimiterHandlerPhoto()


class Statistics:
    _QUEUE = 0
    _KEY_ALL_USER = "all_users"
    _KEY_COUNT_USE_BOT = "count_use_bot"
    _KEY_LIMIT_TRIGGERED = "limit_triggered"
    _lock = threading.Lock()

    @classmethod
    def init(cls):
        if not os.path.isfile(config.STATISTICS_FILE_PATH):
            cls._save_data({Statistics._KEY_ALL_USER: 0, Statistics._KEY_COUNT_USE_BOT: 0,
                            Statistics._KEY_LIMIT_TRIGGERED: 0})

    @classmethod
    def _load_data(cls):
        with cls._lock:
            with open(os.path.join(os.getcwd(), os.path.abspath(config.STATISTICS_FILE_PATH)), "r") as file:
                return json.load(file)

    @classmethod
    def _save_data(cls, data: dict):
        with cls._lock:
            with open(os.path.join(os.getcwd(), os.path.abspath(config.STATISTICS_FILE_PATH)), "w") as file:
                json.dump(data, file)

    @classmethod
    def register(cls):

        data = cls._load_data()
        data[cls._KEY_ALL_USER] += 1
        cls._save_data(data)

    @classmethod
    def use_bot(cls):
        with cls._lock:
            cls._QUEUE += 1
        data = cls._load_data()
        data[cls._KEY_COUNT_USE_BOT] += 1
        cls._save_data(data)

    @classmethod
    def limit_triggered(cls):
        data = cls._load_data()
        data[cls._KEY_LIMIT_TRIGGERED] += 1
        cls._save_data(data)

    @classmethod
    def get_queue(cls):
        with cls._lock:
            return cls._QUEUE

    @classmethod
    def del_queue(cls):
        with cls._lock:
            cls._QUEUE -= 1
