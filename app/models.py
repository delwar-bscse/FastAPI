from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, text
from . database import Base

class Course(Base):
  __tablename__ = "courses"
  id=Column(Integer, primary_key=True, nullable=False)
  name=Column(String, nullable=False)
  instructor=Column(String, nullable=False)
  duration=Column(Float, nullable=False)
  website=Column(String, nullable=False)

class User(Base):
  __tablename__ = "users"
  id=Column(Integer, primary_key=True, nullable=False)
  email=Column(String, nullable=False, unique=True)
  password=Column(String, nullable=False)
  created_at=Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)