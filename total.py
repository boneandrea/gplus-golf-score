from database import *
import sys
from datetime import datetime


class total:
    db = None

    def collect_score(self, query=None):
        client = database().connect_db()
        self.db = client["score"]
        return self.db.score.find(query)

    def sort_by_gross(self):
        query = {
            "date":
            {
                "$gte": datetime(2023, 1, 1),
                "$lt": datetime(2025, 1, 1)
            }
        }
        games = self.collect_score(query)
        average_gross = {}
        point_ranking = {}
        for game in games:
            for scores in game["scores"]:
                if "point" in scores:
                    point = scores["point"]
                else:
                    point = 0

                name = scores["name"]
                gross = int(scores["gross"])
                if name in average_gross:
                    average_gross[name]["gross"] += gross
                    average_gross[name]["game_count"] += 1
                else:
                    average_gross[name] = {
                        "name": name,
                        "gross": gross,
                        "game_count": 1
                    }
                if name in point_ranking:
                    point_ranking[name] += point
                else:
                    point_ranking[name] = point

        to_sort = []
        for name in average_gross:
            average_gross[name]["average"] = round(average_gross[name]["gross"] /
                                                   average_gross[name]["game_count"], 2)
            average_gross[name]["point"] = point_ranking[name]
            to_sort.append(average_gross[name])

        sorted_score = sorted(to_sort, key=lambda x: x["point"], reverse=True)
        result = []
        for index, player in enumerate(sorted_score):
            result.append({
                "rank": index+1,
                "name": player["name"],
                "game_count": player["game_count"],
                "gross": player["average"],
                "point": player["point"]
            })
        return result

    def set_best_gross(self):
        games = self.collect_score()
        for game in games:
            r = sorted(game["scores"], key=lambda x: x["gross"])[0]
            game["scores"][0]["best_gross"] = True
            self.db.score.update_one(
                {"_id": game["_id"]}, {"$set": {"scores": game["scores"]}})

    def count_prizes(self):
        games = self.collect_score()
        self.count_prize(games, "HOLEINONE")
        self.count_prize(games, "ALBATROSS")
        self.count_prize(games, "EAGLE")
        self.count_prize(games, "BIRDIE")

    def count_prize(self, games, prize):
        games.rewind()
        print("================lookup ", prize)
        all_prize = {}
        for game in games:
            for scores in game["scores"]:
                prizes = filter(lambda x: x["prize"] == prize,
                                scores["score"])
                count_prize = len(list(prizes))
                if count_prize > 0:
                    print(scores["name"], prize, count_prize)
                    if scores["name"] in all_prize:
                        all_prize[scores["name"]] += f" {prize} {count_prize}回"

        return all_prize

    def create_html_data(self):
        return self.sort_by_gross()


if __name__ == "__main__":

    x = total()
    x.set_best_gross()
    x.count_prizes()
    x.sort_by_gross()
