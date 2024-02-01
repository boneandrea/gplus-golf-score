from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class database:
    def connect_db(self):
        return MongoClient(os.environ.get('SERVER'),
                           int(os.environ.get('PORT')),
                           username=os.environ['USERNAME'],
                           password=os.environ['PASSWORD'])


# x = Db()
# client = x.connect_db()
# db = client["score"]
# score = db["score"]

# score.insert_one({"fe": 17, "zuba": [3, 3, 4]})

# item = score.find({})
# for i in item:
#     print(i)
