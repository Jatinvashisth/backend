# backend/product/main.py

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from product.routers import login, user
from product.database import Base, engine

from sqlalchemy.exc import OperationalError
import time

app = FastAPI()

# ---------------- PROMETHEUS METRICS ----------------
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total API Requests",
    ["method", "endpoint"]
)

# ---------------- MIDDLEWARE ----------------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    return response


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

# ---------------- ROUTERS ----------------
app.include_router(login.router)
app.include_router(user.router)


# ---------------- DB STARTUP ----------------
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


# ---------------- HEALTH CHECK ----------------
@app.get("/ping")
def root():
    return {"message": "FastAPI backend is running"}


# ---------------- PROMETHEUS ENDPOINT ----------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)