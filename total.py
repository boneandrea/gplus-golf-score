from database import *
import sys


class total:
    db = None

    def collect_score(self):
        client = database().connect_db()
        self.db = client["score"]
        score = self.db.score

        return score.find({})

    def sort_by_gross(self):
        games = self.collect_score()
        average_gross = {}
        for game in games:
            for scores in game["scores"]:
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

        to_sort = []
        for name in average_gross:
            average_gross[name]["average"] = average_gross[name]["gross"] / \
                average_gross[name]["game_count"]
            to_sort.append(average_gross[name])

        return sorted(to_sort, key=lambda x: x["average"])

    def set_best_gross(self):
        games = self.collect_score()
        for game in games:
            r = sorted(game["scores"], key=lambda x: x["gross"])[0]
            game["scores"][0]["best_gross"] = True
            self.db.score.update_one(
                {"_id": game["_id"]}, {"$set": {"scores": game["scores"]}})


if __name__ == "__main__":

    x = total()
    x.set_best_gross()
    sys.exit(0)
    members = x.sort_by_gross()

    for member in members:
        print(member)

    pass
