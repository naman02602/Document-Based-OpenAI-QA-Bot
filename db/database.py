from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mssql+pyodbc://team4admin:team4-bigdata@srv-big-data.database.windows.net/team4bigdata?driver=ODBC+Driver+17+for+SQL+Server"

# Create a new engine instance
engine = create_engine(DATABASE_URL)

# Create a custom session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new instance of the declarative base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
