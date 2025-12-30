from datetime import date, datetime
import argparse
from time import sleep
import pytest
import json
import os
import sys
import re
from database import *


def exec():
    client = database().connect_db()
    db = client["score"]
    member_t = db["members"]
    score = db["score"]
    games = get_data_by_target_year(score)
    average = {}
    for game in games:
        for score in game["scores"]:
            if score["name"] not in average:
                average[score["name"]] = []
            average[score["name"]].append(score["gross"])

    print(average)
    hdcp = {}
    for name in average.keys():
        print(name, average[name], sum(average[name])/len(average[name]))
        hdcp[name] = int((sum(average[name])/len(average[name])-72)*0.7)

    for name in hdcp.keys():
        member = member_t.find_one({"name": name})
        if member == None:
            print(f"{name} is not found")
        else:
            new_hdcp = hdcp[name]
            print(f"{name}: {member['hdcp']} -> NEW {new_hdcp}")
            member_t.update_one(
                {
                    "_id": member["_id"],
                },
                {
                    "$set": {
                        "hdcp": new_hdcp
                    }
                }
            )


def get_data_by_target_year(score):
    # TODO: 過去1年
    # ./a.out 2026 -> 2025 の全データ対象
    year = int(sys.argv[1])-1
    return score.find({
        "date":
        {
            "$gte": datetime(year, 1, 1),
            "$lt": datetime(year + 1, 1, 1)
        }
    })


if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} newyear. exit.")
    sys.exit()

input(f"{sys.argv[1]} の年度切り替えです。OK? || ctrl-c")
input(f"{sys.argv[1]} の年度切り替えです。OK? || ctrl-c")
input(f"{sys.argv[1]} の年度切り替えです。OK? || ctrl-c")
input(f"{sys.argv[1]} の年度切り替えです。OK? || ctrl-c")
input(f"{sys.argv[1]} の年度切り替えです。OK? || ctrl-c")

exec()
