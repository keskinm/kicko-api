from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

engine_path = Path(__file__).parent.parent / "main_engine.db"
DATABASE_URL = f"sqlite:///{engine_path}"
MAIN_ENGINE = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=MAIN_ENGINE)
