import os

from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User


# =========================================================
# JWT SETTINGS
# =========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "mindmirror_local_development_secret"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)


# =========================================================
# PASSWORD SECURITY
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# OAUTH2
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# =========================================================
# HASH PASSWORD
# =========================================================

def hash_password(password):

    return pwd_context.hash(password)


# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(
    password,
    hashed_password
):

    return pwd_context.verify(
        password,
        hashed_password
    )


# =========================================================
# CREATE JWT TOKEN
# =========================================================

def create_access_token(data):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=
                ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate":
                "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )

        user_id = payload.get(
            "user_id"
        )

        if user_id is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception


    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


    if user is None:

        raise credentials_exception


    return user