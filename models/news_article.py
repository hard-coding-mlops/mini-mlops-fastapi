from sqlalchemy import Boolean, Column, Integer, DateTime, String, Text
from sqlalchemy.orm import relationship
from database.conn import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key = True, index = True)
    category = Column(String(10))
    title = Column(String(100))
    content = Column(Text)
    upload_datetime = Column(DateTime)
    scraped_order_no = Column(Integer)
    
    preprocessed_articles = relationship("PreprocessedArticle", back_populates = "news_articles")