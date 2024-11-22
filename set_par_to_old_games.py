from datetime import date, datetime
import argparse
from time import sleep
import pytest
import json
import os
import sys
import re
from database import *


def fix_par():
    client = database().connect_db()
    db = client["score"]
    score = db["score"]

    import dateutil.parser

    games = score.find()
    for game in games:
        pars = [-1]*18
        count_hole_with_par = 0
        for player in game["scores"]:
            for score in player["score"]:
                par = -1
                prize = score.get("prize")
                if prize == "PAR":
                    par = score["score"]
                elif prize == "BOGEY":
                    par = score["score"]-1
                elif prize == "DOUBLEBOGEY":
                    par = score["score"]-2
                elif prize == "TRIPLEBOGEY":
                    par = score["score"]-3
                elif prize == "BIRDIE":
                    par = score["score"]+1
                elif prize == "EAGLE":
                    par = score["score"]+2

                if par != -1:
                    pars[score["hole"]-1] = par

        if len(list(filter(lambda x: x != -1, pars))) == 18:
            update_par(game["_id"], pars)
        else:
            print("fail")


def update_par(game_id, par):
    print(game_id, par)
    client = database().connect_db()
    db = client["score"]
    score = db["score"]
    score.update_one(
        {
            "_id": game_id
        },
        {
            "$set": {"par": par}
        }
    )


fix_par()
