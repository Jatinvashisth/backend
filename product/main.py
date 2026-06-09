# backend/product/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from product.routers import login, user
from product.database import Base, engine
from sqlalchemy.exc import OperationalError
import time

app = FastAPI()

# ---------------- CORS SETUP ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fascinating-truffle-5da5b6.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(user.router)


@app.on_event("startup")
def startup():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("DB Connected & Tables Created")
            break
        except OperationalError:
            print("DB not ready, retrying...")
            time.sleep(3)


@app.get("/ping")
def root():
    return {"message": "FastAPI backend is running"}