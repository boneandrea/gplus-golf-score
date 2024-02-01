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
