from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Try both Railway and MySQL variable prefixes
DB_USER = os.getenv("DB_USER") or os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("DB_HOST") or os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("DB_PORT") or os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("DB_NAME") or os.getenv("MYSQL_DATABASE")

# Validate all env vars
missing = [k for k, v in {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME
}.items() if not v]

if missing:
    raise Exception(f"Database environment variables not set: {', '.join(missing)}")

# Convert port to int safely
DB_PORT = int(DB_PORT)

# Build SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
