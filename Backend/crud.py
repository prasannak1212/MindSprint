from .db import users_collection, habits_collection, logs_collection
from passlib.hash import bcrypt

def create_user(user):
    user["password"] = bcrypt.hash(user["password"])  # hash password
    return users_collection.insert_one(user)

def get_user(username: str):
    return users_collection.find_one({"username": username})

def verify_user(username: str, password: str):
    user = get_user(username)
    if user and bcrypt.verify(password, user["password"]):
        return True
    return False

def create_habit(habit):
    return habits_collection.insert_one(habit)

def get_habits_by_user(username):
    return list(habits_collection.find({'user': username}))

def create_log(log):
    return logs_collection.insert_one(log)

def get_logs_by_user(user, habit_name):
    return list(logs_collection.find({'user':user, 'habit_name':habit_name}))