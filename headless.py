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
"""
Run:

$ pip install -r requirements.e2e.txt
$ pytest -sv test.py # print()あり テスト項目表示あり
$ pytest -v test.py # print()なし テスト項目表示あり
$ pytest test.py # silent
"""

driver = None

# utils


def init_browser():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    options = ChromeOptions()
    options.add_argument("--no-selfandbox")
    options.add_argument("--headless")
    options.set_capability('acceptInsecureCerts', True)
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(
    ).install()), options=options)  # 自動的にSeleniumとChromeバージョンを一致させる


def get_par():
    init_browser()
    driver.get(
        "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a")
    wait = WebDriverWait(driver, timeout=5)
    table = driver.find_elements(By.CSS_SELECTOR, ".sheet table")[0]
    tr = table.find_elements(By.TAG_NAME, "tr")
    td = tr[3].find_elements(By.TAG_NAME, "td")
    par = []
    for t in td:
        par.append(int(t.get_attribute("innerText")))

    par.pop(9)
    par.pop(18)
    return par


def get_igolf(url):
    init_browser()
    driver.get(url)
    driver.get(url.replace("#/landscape-a", "/leaderboard"))
    wait = WebDriverWait(driver, timeout=5)
    show_score_button = driver.find_elements(By.CSS_SELECTOR, ".show-score")
    show_score_button[0].click()
    wait = WebDriverWait(driver, timeout=5)
    table = driver.find_elements(By.CSS_SELECTOR, ".ui-table-view")[0]

    tr = table.find_elements(By.TAG_NAME, "tr")
    num_player = len(tr)-2

    basic_info = get_basic_info()
    scores = {
        "course": basic_info["course"],
        "date": basic_info["date"],
        "scores": []
    }
    par = get_par()

    for i in range(0, num_player):
        tds = tr[i+2].find_elements(By.TAG_NAME, "td")
        score = []
        for td in tds:
            score.append(td.get_attribute("innerText").replace('\u3000', ''))
        score.pop(0)
        del score[1:6]
        score.pop(10)
        score.pop(10)
        score.pop(19)

        data = {
            "name": "",
            "score": []
        }
        name = ""

        for i, s in enumerate(score):
            if i == 0:
                data["name"] = score[i]
            if i > 0 and i < 19:
                data["score"].append({
                    "hole": i,
                    "score": int(score[i]),
                    "prize": prize(par[i-1], int(score[i]))
                })
            if i == 19:
                data["gross"] = int(score[i])

        scores["scores"].append(data)

    return scores


def prize(par, score):
    if score == 1:
        return "HOLEINONE"
    diff = score-par
    match diff:
        case -3:
            return "ALBATROSS"
        case -2:
            return "EAGLE"
        case -1:
            return "BOGEY"
        case 0:
            return "PAR"
        case 1:
            return "BOGEY"
        case 2:
            return "DOUBLEBOGEY"
        case 3:
            return "TRIPLEBOGEY"
        case _:
            return ""


def json_serial(obj):

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {obj} not serializable')


def get_basic_info():

    init_browser()
    driver.get(
        "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a")

    wait = WebDriverWait(driver, timeout=5)
    course = driver.find_elements(By.CSS_SELECTOR, ".cc-name")[
        0].get_attribute("innerText")
    import re
    course = re.sub("^【", "", course)
    course = re.sub("】$", "", course)

    date = driver.find_elements(By.CSS_SELECTOR, ".date")[
        0].get_attribute("innerText")

    # from dateutil.parser import parse
    from datetime import datetime
    date = datetime.strptime(date.replace(
        "プレー日: ", ""), "%Y年%m月%d日").strftime("%Y/%m/%d")

    import dateutil.parser
    date = dateutil.parser.parse(date)

    return {
        "course": course,
        "date": date
    }


scores = get_igolf(sys.argv[1])
print(json.dumps(scores, indent=2, ensure_ascii=False, default=json_serial))
driver.quit()


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


store_score(scores)
