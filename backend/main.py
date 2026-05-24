from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import os

from sqlalchemy.exc import IntegrityError

from .db import engine, SessionLocal
from . import models
from .auth import get_password_hash, verify_password, create_access_token

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str


@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/register")
def register(user: UserIn):
    db = SessionLocal()
    try:
        hashed = get_password_hash(user.password)
        db_user = models.User(username=user.username, hashed_password=hashed)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"msg": "user created", "id": db_user.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User exists")
    finally:
        db.close()


@app.post("/auth/login")
def login(user: UserIn):
    db = SessionLocal()
    try:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(user.username)
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()


