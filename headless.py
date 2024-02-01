from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import date, datetime
from time import sleep
import pytest
import json
import os
import sys
import re
from database import *
from igolf import *
from marshalI import *
"""
Run:

$ pip install -r requirements.e2e.txt
$ pytest -sv test.py # print()あり テスト項目表示あり
$ pytest -v test.py # print()なし テスト項目表示あり
$ pytest test.py # silent
"""


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {obj} not serializable')


def store_score(result):
    client = database().connect_db()
    db = client["score"]
    score = db["score"]

    import dateutil.parser
    dateStr = "2016-11-11"
    d = dateutil.parser.parse(dateStr)
    score.insert_one(result)

    item = score.find({})
    for i in item:
        print(i)


# x = igolf()
# scores = x.get_scores(sys.argv[1])
# print(json.dumps(scores, indent=2, ensure_ascii=False, default=json_serial))

x = marshalI()
scores = x.get_scores(sys.argv[1])
print(json.dumps(scores, indent=2, ensure_ascii=False, default=json_serial))

store_score(scores)
