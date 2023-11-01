from datetime import datetime
from sqlalchemy import BIGINT, Column, Float, Integer, String, DateTime
from sqlalchemy.sql import func

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True)
    last_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.now())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now(), onupdate=datetime.now())


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    category_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.now())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now(), onupdate=datetime.now())


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.now())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now(), onupdate=datetime.now())
