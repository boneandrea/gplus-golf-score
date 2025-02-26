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

    def count_games_by_player(self):
        year = date.today().year
        games = self.collect_score({
            "date":
            {
                "$gte": datetime(year-1, 1, 1),
            }
        })
        members = list(self.db.members.find())
        target_members = {}
        for game in games:
            for member in members:
                name = member["name"]
                if len(list(filter(lambda x: x["name"] == name, game["scores"]))) > 0:
                    if name not in target_members:
                        target_members[name] = 1
                    else:
                        target_members[name] += 1

        less_members = []
        for name, hdcp in target_members.items():
            if hdcp < 5:
                less_members.append({name: hdcp})

        return less_members


if __name__ == "__main__":

    x = total()
    x.set_best_gross()
    x.count_prizes()
    x.sort_by_gross()
