from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("SECRET_KEY", "dev-secret")
JWT_ALGORITHM = "HS256"


class UserIn(BaseModel):
    username: str
    password: str


fake_user_db = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


def create_access_token(sub: str, expires_minutes: int = 60):
    to_encode = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


@app.post("/auth/register")
async def register(user: UserIn):
    if user.username in fake_user_db:
        raise HTTPException(status_code=400, detail="User exists")
    hashed = pwd_context.hash(user.password)
    fake_user_db[user.username] = {"username": user.username, "password": hashed}
    return {"msg": "user created"}


@app.post("/auth/login")
async def login(user: UserIn):
    record = fake_user_db.get(user.username)
    if not record or not pwd_context.verify(user.password, record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

