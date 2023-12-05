from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base

class Model(Base):
    __tablename__ = "models"

    model_id = Column(Integer, primary_key = True, index = True)
    model_name = Column(Text)
    
    graphs = relationship("Graph", back_populates = "models")
    epochs = relationship("Epoch", back_populates = "models")