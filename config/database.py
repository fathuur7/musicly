from pymongo import MongoClient
import os
import sys

def connect_db():
    try:
        mongo_uri = os.environ.get('MONGO_URI')
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        print(f"MongoDB Connected: {client.address}")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)
