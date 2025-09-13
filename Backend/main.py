from fastapi import FastAPI, HTTPException
from .schemas import User, Habit, Log
from .crud import create_user, create_habit, get_habits_by_user, create_log, get_logs_by_user, get_user, verify_user
from .db import users_collection, habits_collection, logs_collection

app = FastAPI()

@app.get('/')
def root():
    return {'status':200, 'message':'FastAPI server running'}

def clean_mongodb_doc(doc):
    doc = dict(doc)
    if "_id" in doc:
        doc['_id']= str(doc['_id'])
    return dict(doc)


@app.post('/add_user')
def add_user(user: User):
    try:
        user_dict = user.model_dump()
        create_crud = create_user(user_dict)
        inserted_user = users_collection.find_one({'_id':create_crud.inserted_id})
        inserted_user = clean_mongodb_doc(inserted_user)
        return {'status':'success', 'data':inserted_user, "message" :'User created successfully!'}
    except Exception as e:
        return {'status':'failure', 'message': 'Add user failed'}

@app.post('/add_habit')
def add_habit(habit: Habit):
    try:
        habit_dict = habit.model_dump()
        result = create_habit(habit_dict)
        inserted_habit = habits_collection.find_one({'_id': result.inserted_id})
        inserted_habit = clean_mongodb_doc(inserted_habit)
        return {'status':'success', 'data':inserted_habit, 'message':'Habit created successfully!'}
    except Exception as e:
        return {'status':'failure', 'message':'Add habit failed'}

@app.get('/habits/{username}')
def get_habits(username: str):
    try: 
        result = [clean_mongodb_doc(h) for h in get_habits_by_user(username)]
        return {'status':'success', 'data':result, 'message':'Habits fetched successfully!'}
    except Exception as e:
        return {'status':'failure', 'message':'Fetch Habits failed'}
    
@app.post('/add_log')
def add_log(log: Log):
    try:
        log_dict = log.model_dump()
        result = create_log(log_dict)
        inserted_log = logs_collection.find_one({'_id':result.inserted_id})
        inserted_log = clean_mongodb_doc(inserted_log)
        return {'status': 'success', 'data': inserted_log, 'message':'Log created successfully!'}
    except Exception as e:
        return {'status': 'failure', 'message': 'Add log failed'}
    
@app.get('/logs/{username}/{habit_name}')
def get_logs(username: str, habit_name: str):
    try:
        result = [clean_mongodb_doc(l) for l in get_logs_by_user(username, habit_name)]
        return {'status':'success', 'data':result, 'message':'Logs fetched successfully!'}
    except Exception as e:
        return {'status':'failure', 'message':'Get logs failed'}
    
@app.post("/login/")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if verify_user(username, password):
        return {"message": "Login successful"}
    # raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/users/")
def signup(user: dict):
    existing = get_user(user["username"])
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(user)
    return {"message": "User created successfully"}


