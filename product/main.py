from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, login, user
from fastapi.middleware.cors import CORSMiddleware

# ✅ Create DB tables
models.Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Allowed origins (Frontend URLs)
origins = [
    "http://localhost:5173",                         # Local React
    "https://vashisth1234.netlify.app",              # ✅ Your live Netlify
]

# ✅ Add CORS middleware (must come BEFORE routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers (AFTER CORS setup)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(login.router)
