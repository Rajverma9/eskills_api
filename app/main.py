from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy.exc import OperationalError
from app.database import engine, create_db_and_tables
from app.routers import course,auth
from app.seed.run_seed import run_seed

app = FastAPI(title="Course Management API",)


@app.on_event("startup")
def startup():
    try:
        create_db_and_tables()
        print("Database Connected Successfully!")

    except OperationalError as e:
        print("Database Connection Failed:", e)
        run_seed()


app.include_router(course.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Course Management API is running"}