from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str

class Habit(BaseModel):
    user: str
    habit_name: str
    description: Optional[str] = None

class Log(BaseModel):
    user: str
    habit_name: str
    date: str
    status: Optional[str] = "done"
    # value: Optional[str] = None