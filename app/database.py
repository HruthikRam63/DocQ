from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./docq.db"

# Creating a SQLAlchemy engine to interact with the SQLite database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Creating a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database (create tables)."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()