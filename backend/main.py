from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from database import models

from routes import auth
from routes import chat


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="MindMirror AI"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================================
# AUTH ROUTES
# =====================================================

app.include_router(
    auth.router
)


# =====================================================
# CHAT ROUTES
# =====================================================

app.include_router(
    chat.router,
    prefix="/chat"
)


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "message": "MindMirror AI is running"
    }