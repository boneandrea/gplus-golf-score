from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class database:
    def connect_db(self):
        return MongoClient(os.environ.get('DB_SERVER'),
                           int(os.environ.get('DB_PORT')),
                           username=os.environ['DB_USERNAME'],
                           password=os.environ['DB_PASSWORD'])
