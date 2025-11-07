from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv  # pip install python-dotenv

# Load .env if exists (local development)
load_dotenv()

# Read environment variables
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DATABASE")

# Safety check
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise Exception("Database environment variables are not properly set!")

# Convert port to integer
DB_PORT = int(DB_PORT) if DB_PORT else 3306

# SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Debug log (remove in production)
print("Connecting to:", SQLALCHEMY_DATABASE_URL)

# Create engine and session
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
