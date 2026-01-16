from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from app.schemas.task import TaskRead


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    tasks: List[TaskRead] = []
    model_config = ConfigDict(from_attributes=True)


class UserWithTasks(UserRead):
    tasks: List[TaskRead] = []