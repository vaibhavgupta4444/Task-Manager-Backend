from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import users, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "FastAPI modular project running with lifespan events"}
