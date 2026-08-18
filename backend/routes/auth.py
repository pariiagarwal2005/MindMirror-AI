from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User

from core.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter()



@router.post("/register")
def register(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return {
        "message": "User created successfully",
        "id": new_user.id
    }




@router.post("/login")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )


    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )



    if not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )



    token = create_access_token(
        {
            "user_id": user.id
        }
    )


    return {

        "access_token": token,

        "token_type": "bearer"

    }