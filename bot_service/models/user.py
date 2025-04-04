from sqlalchemy import Column, Integer, Text
from database.db_config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Text)
