import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# DYNAMIC TARGET: Check if pytest is running the environment
if "pytest" in sys.modules:
    DATABASE_URL = "sqlite:///:memory:"
    # StaticPool forces SQLAlchemy to maintain one shared memory connection across all paths
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    # Your real production PostgreSQL configuration layout
    DATABASE_URL = "postgresql://apple@localhost:5432/streakifyv1_db"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()