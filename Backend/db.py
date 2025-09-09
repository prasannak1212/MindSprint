from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["habit_tracker"]

users_collection = db["users"]
habits_collection = db["habits"]
logs_collection = db["logs"]
