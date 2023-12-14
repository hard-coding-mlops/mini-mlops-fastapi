from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text,String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.conn import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    client_id = Column(Integer, primary_key = True, index = True)
    model_id = Column(Integer, ForeignKey("models.model_id"))
    
    models = relationship("Model", back_populates = "users")