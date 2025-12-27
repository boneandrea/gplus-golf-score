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

    import dateutil.parser

    # print(member["hdcp"])
    # if type(game["date"]) == str:
    #     member.update_one(
    #         {
    #             "_id": game["_id"],
    #         },
    #         {
    #             "$set": {"date": dateutil.parser.parse(game["date"])}
    #         }
    #     )
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
            print(f"{name}: {member['hdcp']} -> NEW {hdcp[name]}")

    # members=member_t.find()
    # for member in members:
    #     print(member)


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


exec()
