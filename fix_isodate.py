from datetime import date, datetime
import argparse
from time import sleep
import pytest
import json
import os
import sys
import re
from database import *
from igolf import *
from marshalI import *


def fix_date():
    client = database().connect_db()
    db = client["score"]
    score = db["score"]

    import dateutil.parser

    games = score.find()
    for game in games:
        if type(game["date"]) == str:
            score.update_one(
                {
                    "_id": game["_id"],
                },
                {
                    "$set": {"date": dateutil.parser.parse(game["date"])}
                }
            )


fix_date()
