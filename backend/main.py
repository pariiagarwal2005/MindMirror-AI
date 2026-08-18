import os

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from database.database import (
    Base,
    engine,
    ensure_database
)

from database import models

from routes import auth
from routes import chat


# =====================================================
# DATABASE
# =====================================================

Base.metadata.create_all(
    bind=engine
)

ensure_database()


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="MindMirror AI",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    ""
)


allowed_origins = [

    "http://localhost:5173",

    "http://127.0.0.1:5173"

]


if FRONTEND_URL:

    allowed_origins.append(
        FRONTEND_URL.rstrip("/")
    )


app.add_middleware(

    CORSMiddleware,

    allow_origins=
        allowed_origins,

    allow_credentials=
        True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]

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
# HEALTH CHECK
# =====================================================

@app.get("/")
def home():

    return {

        "message":
            "MindMirror AI is running",

        "status":
            "healthy"

    }


@app.get("/health")
def health():

    return {

        "status":
            "healthy"

    }