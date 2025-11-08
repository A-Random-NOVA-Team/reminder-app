# run this file to create missing tables in the database
from core.config import get_settings
from sqlalchemy import create_engine
from .base import Base

engine = create_engine(get_settings().sqlalchemy_database_uri.replace("+aiosqlite", ""))
Base.metadata.create_all(bind=engine)  # pass in the engine
