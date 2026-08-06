from fastapi import FastAPI

from database.database import engine, Base
from database import models

from routes import journal


app = FastAPI(
    title="MindMirror AI",
    description="Personal AI Reflection and Mental Wellness Companion"
)


Base.metadata.create_all(bind=engine)


app.include_router(journal.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MindMirror AI"
    }