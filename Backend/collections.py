from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str

class Habit(BaseModel):
    user: str
    habit_name: str
    decsription: Optional[str] = None

class Log(BaseModel):
    user: str
    habit_name: str
    date: str
    status: Optional[str] = "done"
    value: Optional[str] = None