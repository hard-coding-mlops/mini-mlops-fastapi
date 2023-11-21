from sqlalchemy import Boolean, Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base
    
class PreprocessedArticle(Base):
    __tablename__ = "preprocessed_articles"
    
    id = Column(Integer, primary_key = True, index = True)
    news_article_id = Column(Integer, ForeignKey("news_articles.id"))
    category_no = Column(Integer)
    embedded_inputs = Column(Text)
    
    news_articles = relationship("NewsArticle", back_populates = "preprocessed_articles")