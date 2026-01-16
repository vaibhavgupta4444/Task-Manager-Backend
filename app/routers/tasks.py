from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskRead
from app.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    db_task = Task(**task.model_dump(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task