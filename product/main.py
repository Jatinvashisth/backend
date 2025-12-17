from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import product, login, user

# --- Create all tables if they don't exist ---
models.Base.metadata.create_all(bind=engine)

# --- Initialize FastAPI ---
app = FastAPI(title="Backend API", version="1.0")

# --- Allowed origins (frontend URLs) ---
origins = [
    "https://vashisth1234.netlify.app",
    "http://localhost:5173",
]

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include routers ---
app.include_router(product.router)
app.include_router(user.router)
app.include_router(login.router)

# --- Health check route ---
@app.get("/ping")
def ping():
    return {"message": "CORS setup working ✅"}
