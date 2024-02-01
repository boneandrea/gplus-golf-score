from database import *


class total:
    def collect_score(self):
        client = database().connect_db()
        db = client["score"]
        score = db["score"]

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


if __name__ == "__main__":

    x = total()
    members = x.sort_by_gross()

    for member in members:
        print(member)

    pass
