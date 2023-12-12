from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text,String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.conn import Base
from datetime import datetime
class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key = True, index = True)
    model_id = Column(Integer, ForeignKey("models.model_id"))
    use_at = Column(DateTime, default = datetime.now())
    user_insert = Column(Text, default = False)
    predict_result = Column(String(10), default = False)
    client_result = Column(String(10), default = '-')
    
    models = relationship("Model", back_populates = "clients")