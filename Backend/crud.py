from .db import users_collection, habits_collection, logs_collection

def create_user(user):
    return users_collection.insert_one(user)

def create_habit(habit):
    return habits_collection.insert_one(habit)

def get_habits_by_user(username):
    return list(habits_collection.find({'user': username}))

def create_log(log):
    return logs_collection.insert_one(log)

def get_logs_by_user(user, habit_name):
    return list(logs_collection.find({'user':user, 'habit_name':habit_name}))