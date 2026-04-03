from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCAMY_DATABASE_URL = "sqlite:///./blog.db"

enngine = create_engine(
    SQLALCAMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=enngine)

class Base(DeclarativeBase):
    pass

def get_db():
   with SessionLocal() as db:
    try:
        yield db
    finally:
        db.close()



