from datetime import date, datetime
import argparse
from time import sleep
import pytest
import json
import os
import sys
import re
from database import *


def execute():
    client = database().connect_db()
    db = client["score"]
    score = db["score"]

    import dateutil.parser

    games = score.find()
    for game in games:
        for i, s in enumerate(game["scores"]):
            game["scores"][i]["name"] = s["name"]            .replace(
                " ", "")            .replace("　", "")
        print(game)

        score.update_one(
            {
                "_id": game["_id"],
            },
            {
                "$set": {"scores": game["scores"]}
            }
        )


execute()
