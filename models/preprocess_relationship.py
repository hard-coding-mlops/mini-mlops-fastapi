from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base

class PreprocessRelationship(Base):
    __tablename__ = "preprocess_relationships"
    
    id = Column(Integer, primary_key = True, index = True)
    news_article_id = Column(Integer, ForeignKey("news_articles.id"))
    preprocessed_article_id = Column(Integer, ForeignKey("preprocessed_articles.id"))
    
    news_articles = relationship("NewsArticle", back_populates = "preprocess_relationships")
    preprocessed_articles = relationship("PreprocessedArticle", back_populates = "preprocess_relationships")