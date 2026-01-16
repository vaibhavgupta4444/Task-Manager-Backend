from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserRead
from sqlalchemy.orm import Session, selectinload
from app.dependencies import get_db, get_current_user
from app.models import User
from app.core.security import get_password_hash, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# protected route
@router.get("/")
def fetch_users(db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):
    is_admin = db.query(User).filter(User.id == current_user['sub'], User.role == 'admin').first()

    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="only admin can access these routes")
    
    all_users = db.query(User).options(selectinload(User.tasks)).all()
    return all_users


# Public routes
@router.post("/register")
def create_user(user: UserCreate,
                db: Session = Depends(get_db)):
    is_user_exist = db.query(User).filter(User.email == user.email).first()
    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid username or password")
    hashed_password = get_password_hash(user.password)
    user_data = user.model_dump()
    user_data.pop("password")    
    new_user = User(**user_data, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "success": True,
        "Message": "User created Successfully"
    }


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
