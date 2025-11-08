from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import product, login, user

# --- Create all database tables ---
models.Base.metadata.create_all(bind=engine)

# --- Initialize FastAPI app ---
app = FastAPI(title="Backend API", version="1.0")

# --- Allowed origins (frontend URLs) ---
origins = [
    "https://vashisth1234.netlify.app",   # ✅ Deployed Netlify frontend
    "https://www.vashisth1234.netlify.app",  # (optional) Netlify "www" redirect case
    "http://localhost:5173",              # ✅ Local dev (Vite/React)
]

# --- CORS Middleware (MUST come before routers) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # specify allowed origins
    allow_credentials=True,       # allow cookies / auth headers
    allow_methods=["*"],          # allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],          # allow all headers (Content-Type, Authorization, etc.)
)

# --- Include routers (AFTER middleware) ---
app.include_router(product.router)
app.include_router(user.router)
app.include_router(login.router)

# --- Health check / CORS test route ---
@app.get("/ping")
def ping():
    return {"message": "CORS setup working ✅"}
