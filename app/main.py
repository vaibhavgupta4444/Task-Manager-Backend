from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

@app.get("/")
def root():
    return {"message": "FastAPI Task Manager Running"}
