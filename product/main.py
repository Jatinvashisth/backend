# backend/product/main.py
from fastapi import FastAPI
from product.routers import login, user
from fastapi.middleware.cors import CORSMiddleware
from product.database import Base, engine
import time
from sqlalchemy.exc import OperationalError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        
                   "http://3.23.7.21:8000",
                   "http://frontend-2026-deploy.s3-website.us-east-2.amazonaws.com"
                   
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(user.router)


@app.on_event("startup")
def startup():
    # DB wait + retry (IMPORTANT for docker)
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