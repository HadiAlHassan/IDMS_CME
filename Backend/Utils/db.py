from pymongo import MongoClient
from django.conf import settings

class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
            cls._instance.db = client[settings.DATABASES['default']['NAME']]
        return cls._instance.db

def connect_to_mongo():
    return MongoConnection()