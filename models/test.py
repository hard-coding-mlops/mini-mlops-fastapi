from sqlalchemy import Column, Integer, Text, String
from database.conn import Base

class Test(Base):
    __tablename__ = "tests"

    test_id = Column(Integer, primary_key = True, index = True)
    quest = Column(Text, default = False)
    answer = Column(String(10), default = False)
    predict = Column(String(10), default = False)
    answer = Column(String(10), default = False)