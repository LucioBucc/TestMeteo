from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# Creazione engine per connetterci a MySQL
engine = create_engine(config("DATABASE_URL"))

connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()