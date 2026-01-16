from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Task, User
from app.schemas import TaskCreate, TaskRead, TaskUpdate
from app.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/", response_model = list[TaskRead])
def get_tasks(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.owner_id == current_user['sub'])
    return tasks


@router.post("/")
def create_task(task: TaskCreate,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    isOwnerExist = db.query(User).filter(User.id == current_user['sub']).first()

    if not isOwnerExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    db_task = Task(**task.model_dump(), owner_id=current_user['sub'])
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task



@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    db_task = (
        db.query(Task)
        .filter(
            Task.owner_id == current_user["sub"],
            Task.id == task_id
        )
        .first()
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.completed is not None:
        db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)

    return db_task


# Tasks that only performed by admin
@router.delete("/{task_id}", response_model=TaskRead)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    is_admin = db.query(User).filter(User.id == current_user['sub'], User.role == 'admin').first()

    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="only admin can access these routes")
    
    db_task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(db_task)

    db.commit()
    return 