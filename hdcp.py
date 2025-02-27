from datetime import datetime, date
import sys
from util import *
from database import *


class hdcp:
    db = None

    def __init__(self):
        self.client = database().connect_db()
        self.db = self.client["score"]

    def log(self, *msg):
        if self.verbose:
            print(*msg)

    def update_html(self, template):
        members = sorted(list(self.db.members.find()),
                         key=lambda x: (x["hdcp"]))
        year = date.today().year
        result = template.render(
            title=f"HDCP: 水曜ゴルフGP {year}",
            year=year,
            msg="",
            members=members,
        )

        dir = "docs/%s" % year

        if os.path.isdir(dir):
            pass
        else:
            os.mkdir(dir)

        path = "%s/hdcp.html" % dir

        with open(path, 'w') as f:
            f.write(result)

        # 5回未満の人は再計算
        self.update_hdcp()
        sys.exit(0)

    def update_hdcp(self):
        candidates = self.find_members_with_less_than_5games()
        print(candidates)
        for member in candidates:
            average = self.calculate_average_for_member(member)
            hdcp = self.calc_hdcp(average)
            hdcp_in_db = self.db.members.find_one({"name": member["name"]})
            print("CALCLATED HD:", hdcp)
            member["hdcp"] = hdcp
            if hdcp_in_db == None:
                self.create_new_member(member)
            else:
                self.update_new_member(member, hdcp_in_db)
        # - [x] calculate_average for each member
        # - [ ] use smaller value
        # - [ ] save
        print(candidates)

    def calculate_average_for_member(self, member):
        print("-------------")
        print("A", member)
        year = date.today().year
        games = self.collect_score({
            "date":
            {
                "$gte": datetime(year - 1, 1, 1),
            }
        })
        gross = 0
        for game in games:
            for score in game["scores"]:
                if member["name"] == score["name"]:
                    gross += score["gross"]

        average = gross / member["count"]
        print(gross, member["count"], average)
        return average

    def create_new_member(self, member):
        del (member["count"])
        print("------------> NEW MEMBER:", member)
        self.db.members.insert_one(member)

    def update_new_member(self, member, before):
        del (member["count"])
        print("------- 0.7,0.8は先？あと？-----> UPDATE MEMBER:", member, before)

    def calc_hdcp(self, average):
        return int((average - 72) * 0.7)

    def collect_score(self, query={}):
        default_query = self.default_query()
        default_query.update(query)
        return list(self.db.score.find(default_query))

    def default_query(self):
        year = date.today().year
        return {
            "date":
            {
                "$gte": datetime(year, 1, 1),
                "$lt": datetime(year + 1, 1, 1)
            }
        }

    def find_members_with_less_than_5games(self):
        return self.count_games_by_player()

    def find_members_last_game(self):
        last_game = list(self.db.score.find().sort("date", -1).limit(1))
        members = list(map(lambda x: x["name"], last_game[0]["scores"]))
        print(members)
        return members

    def count_games_by_player(self):
        year = date.today().year
        games = self.collect_score({
            "date":
            {
                "$gte": datetime(year - 1, 1, 1),
            }
        })
        # TODO:
        # - [ ] 参加者のみ
        members = self.find_members_last_game()
        target_members = {}
        for game in games:
            for name in members:
                if len(list(filter(lambda x: x["name"] == name, game["scores"]))) > 0:
                    if name not in target_members:
                        target_members[name] = 1
                    else:
                        target_members[name] += 1

        less_members = []
        for name, count in target_members.items():
            if count < 5:
                less_members.append({"name": name, "count": count})

        return less_members


if __name__ == "__main__":

    x = total()
    x.set_best_gross()
    x.count_prizes()
    x.sort_by_gross()
