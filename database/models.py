from sqlalchemy import BIGINT, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True)
    platform_type = Column(String, nullable=False)
    platform_user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=DateTime.utcnow)


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=DateTime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
