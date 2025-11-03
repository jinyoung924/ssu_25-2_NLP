from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    publisher = Column(String, index=True)
    score = Column(Float)