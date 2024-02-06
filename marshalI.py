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
from util import *
"""
マーシャルアイクラウド解析
ホールバイホールからデータ取得
"""


class marshalI:
    driver = None

    def __init__(self, url):
        self.url = url

    def init_browser(self):
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['acceptInsecureCerts'] = True
        options = ChromeOptions()
        options.add_argument("--no-selfandbox")
        options.add_argument("--headless")
        options.set_capability('acceptInsecureCerts', True)
        global driver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(
        ).install()), options=options)  # 自動的にSeleniumとChromeバージョンを一致させる

    def get_par(self, table):
        tr = table.find_elements(By.CSS_SELECTOR, "thead tr")[1]
        th = tr.find_elements(By.TAG_NAME, "th")
        return list(map(lambda e: int(e.get_attribute("innerText")), th))

    def get_scores(self):
        self.init_browser()
        driver.get(self.url)
        wait = WebDriverWait(driver, timeout=5)
        table = driver.find_element(
            By.CSS_SELECTOR, "table.holebyholeTable")
        tr = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        d = driver.find_element(
            By.CSS_SELECTOR, ".panel-heading").get_attribute("innerText")
        m = re.match(r'((.|\s)*)プレー日：((.|\s)*)', d)
        course = m[1].strip()
        date = m[3].strip()
        par = self.get_par(table)
        from datetime import datetime
        import dateutil.parser
        date = datetime.strptime(date, "%Y年%m月%d日").strftime("%Y/%m/%d")
        date = dateutil.parser.parse(date)

        results = {
            "course": course,
            "date": date,
            "par": sum(par),
            "scores": []
        }
        num_player = len(tr)-1

        for i in range(0, num_player):
            name = tr[i].find_elements(By.TAG_NAME, "td")[
                1].get_attribute("innerText").replace('\u3000', '')
            td = tr[i].find_elements(By.TAG_NAME, "td")
            score = []
            for j in range(0, 20):
                score.append(
                    td[3+j].find_element(By.TAG_NAME, "span").get_attribute("data-par"))

            score.pop(9)
            score.pop(18)

            scores = {
                "name": name,
                "score": [],
                "gross": 0
            }

            gross = 0
            for i, s in enumerate(score):
                scores["score"].append({
                    "hole": i+1,
                    "score": int(score[i])+int(par[i-1]),
                    "prize": prize(par[i-1], int(score[i])+int(par[i-1]))
                })
                scores["gross"] += int(score[i])+int(par[i-1])

            results["scores"].append(scores)
        driver.quit()
        return results
