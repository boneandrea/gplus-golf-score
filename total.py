from database import *
from util import *
import sys
from datetime import datetime


class total:
    db = None

    def collect_score(self, query={}):
        client = database().connect_db()
        self.db = client["score"]
        default_query = self.default_query()
        default_query.update(query)
        return list(self.db.score.find(default_query))

    def default_query(self):
        return {
            "date":
            {
                "$gte": datetime(2023, 1, 1),
                "$lt": datetime(2025, 1, 1)
            }
        }

    def sort_by_gross(self):
        bestscore = {"name": "", "gross": 300}
        games = self.collect_score()
        average_gross = {}
        point_ranking = {}
        for game in games:
            point_by_game = {}
            for scores in game["scores"]:
                if "point" in scores:
                    point = scores["point"]
                else:
                    point = 0

                name = scores["name"]
                gross = int(scores["gross"])
                if gross < bestscore["gross"]:
                    bestscore["gross"] = gross
                    bestscore["name"] = name

                if name in average_gross:
                    average_gross[name]["gross"] += gross
                    average_gross[name]["game_count"] += 1
                else:
                    average_gross[name] = {
                        "name": name,
                        "gross": gross,
                        "game_count": 1
                    }
                point_by_game[name] = point

            point_by_game = sorted(point_by_game.items(), key=lambda kv:
                                   (kv[1]), reverse=True)
            print(point_by_game)
            point_by_game = self.add_leaders_point(point_by_game)
            print(point_by_game)

            for point in point_by_game:
                name = point[0]
                if not name in point_ranking:
                    point_ranking[name] = 0
                point_ranking[name] += point[1]
            print(point_ranking)

        print(point_ranking)

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
        return {"result": result, "bestscore": bestscore}

    def set_best_gross(self):
        games = self.collect_score()
        for game in games:
            r = sorted(game["scores"], key=lambda x: x["gross"])[0]
            game["scores"][0]["best_gross"] = True
            self.db.score.update_one(
                {"_id": game["_id"]}, {"$set": {"scores": game["scores"]}})

    def merge_prizes(self, ranking, prizes):
        for player in ranking:
            if player["name"] in prizes:
                player["prize_list"] = prizes[player["name"]]["text"]
                player["nearpin"] = int(prizes[player["name"]]["nearpin"])
        return ranking

    def count_prizes(self):
        games = self.collect_score()
        all_prize = {}
        all_prize = self.count_prize(games, "HOLEINONE", all_prize=all_prize)
        all_prize = self.count_prize(games, "ALBATROSS", all_prize=all_prize)
        all_prize = self.count_prize(games, "EAGLE", all_prize=all_prize)
        all_prize = self.count_prize(games, "BIRDIE", all_prize=all_prize)
        all_prize = self.count_nearpin(games, all_prize=all_prize)

        result = {}
        for name in all_prize:
            prizes = []
            for prize in all_prize[name]:
                if prize == "nearpin":
                    pass
                else:
                    prizes.append(f"{PRIZE[prize]} {all_prize[name][prize]}")

            result[name] = {
                "text": ", ".join(prizes),
                "nearpin": all_prize[name]["nearpin"]
            }
        return result

    def count_prize(self, games, prize, all_prize={}):
        for game in games:
            count_prize = 0
            for scores in game["scores"]:
                name = scores["name"]

                prizes = filter(lambda x: x["prize"] == prize,
                                scores["score"])
                count_prize = len(list(prizes))

                if not name in all_prize:
                    all_prize[name] = {}

                if count_prize > 0:
                    if prize in all_prize[name]:
                        all_prize[name][prize] += count_prize
                    else:
                        all_prize[name][prize] = count_prize

        return all_prize

    def count_nearpin(self, games, all_prize={}):
        for game in games:
            count_prize = 0
            for scores in game["scores"]:
                name = scores["name"]
                nearpin = self.find_nearpin(scores)

                if not "nearpin" in all_prize[name]:
                    all_prize[name]["nearpin"] = 0
                all_prize[name]["nearpin"] += nearpin
        return all_prize

    def find_nearpin(self, scores):
        nearpin = 0
        if "near0" in scores:
            nearpin += 1
        if "near1" in scores:
            nearpin += 1
        if "near2" in scores:
            nearpin += 1
        if "near3" in scores:
            nearpin += 1
        return nearpin

    def add_leaders_point(self, points):
        points[0] = (points[0][0], points[0][1]+5)
        points[1] = (points[1][0], points[1][1]+3)
        points[2] = (points[2][0], points[2][1]+1)
        return points

    def create_html_data(self):
        return self.sort_by_gross()


if __name__ == "__main__":

    x= total()
    x.set_best_gross()
    x.count_prizes()
    x.sort_by_gross()
