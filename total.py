from database import *
from util import *
import sys
from datetime import datetime


class total:
    db = None

    def collect_score(self, query=None):
        client = database().connect_db()
        self.db = client["score"]
        return list(self.db.score.find(query))

    def sort_by_gross(self):
        bestscore={"name":"","gross":300}
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
                if gross < bestscore["gross"]:
                    bestscore["gross"]=gross
                    bestscore["name"]=name

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
        return {"result":result,"bestscore":bestscore}

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
                player["prize_list"]=prizes[player["name"]]["text"]
                player["nearpin"]=int(prizes[player["name"]]["nearpin"])
        return ranking

    def count_prizes(self):
        games = self.collect_score()
        all_prize=self.count_prize(games, "HOLEINONE")
        all_prize=self.count_prize(games, "ALBATROSS",all_prize=all_prize)
        all_prize=self.count_prize(games, "EAGLE",all_prize=all_prize)
        all_prize=self.count_prize(games, "BIRDIE",all_prize=all_prize)

        result={}
        for name in all_prize:
            prizes=[]
            for prize in all_prize[name]:
                if prize == "nearpin":
                    pass
                else:
                    prizes.append(f"{PRIZE[prize]} {all_prize[name][prize]}")

            result[name]={
                "text":", ".join(prizes),
                "nearpin": all_prize[name]["nearpin"]
            }
        return result

    def count_prize(self, games, prize, all_prize={}):
        for game in games:
            count_prize=0
            for scores in game["scores"]:
                nearpin=0
                name=scores["name"]
                if "near0" in scores:
                    nearpin+=1
                if "near1" in scores:
                    nearpin+=1
                if "near2" in scores:
                    nearpin+=1
                if "near3" in scores:
                    nearpin+=1

                prizes = filter(lambda x: x["prize"] == prize,
                                scores["score"])
                count_prize= len(list(prizes))

                if not name in all_prize:
                    all_prize[name]={}

                if count_prize > 0:
                    if prize in all_prize[name]:
                        all_prize[name][prize]+=count_prize
                    else:
                        all_prize[name][prize]=count_prize

                all_prize[name]["nearpin"]=nearpin

        return all_prize

    def create_html_data(self):
        return self.sort_by_gross()


if __name__ == "__main__":

    x = total()
    x.set_best_gross()
    x.count_prizes()
    x.sort_by_gross()
