from pymongo import MongoClient
from app.config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)

db = client[DB_NAME]

users_collection = db["users"]
reports_collection = db["reports"]
alerts_collection = db["alerts"]