from pymongo import MongoClient
from django.conf import settings
from gridfs import GridFS

class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
            cls._instance.db = client[settings.DATABASES['default']['NAME']]
        return cls._instance.db

class GridFSConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GridFSConnection, cls).__new__(cls)
            db = MongoConnection()
            cls._instance.fs = GridFS(db)
        return cls._instance.fs

def connect_to_mongo():
    return MongoConnection()

def connect_to_gridfs():
    return GridFSConnection()