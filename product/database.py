import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Railway environment variables
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "railway")

# Ensure port is int
try:
    MYSQL_PORT = int(MYSQL_PORT)
except ValueError:
    raise ValueError(f"Invalid MYSQL_PORT: {MYSQL_PORT}")

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Session & Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
