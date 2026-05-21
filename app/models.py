from sqlalchemy import Column, Integer, String, Float
from . database import Base

class Course(Base):
  __tablename__ = "course"
  id=Column(Integer, primary_key=True, nullable=False)
  name=Column(String, nullable=False)
  instructor=Column(String, nullable=False)
  duration=Column(Float, nullable=False)
  website=Column(String, nullable=False)