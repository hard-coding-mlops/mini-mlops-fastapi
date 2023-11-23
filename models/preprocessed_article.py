from sqlalchemy import Boolean, Column, Integer, DateTime, String, Text
from sqlalchemy.orm import relationship
from database.conn import Base
    
class PreprocessedArticle(Base):
    __tablename__ = "preprocessed_articles"
    
    id = Column(Integer, primary_key = True, index = True)
    category_no = Column(Integer)
    embedded_inputs = Column(Text)
    
    preprocess_relationships = relationship("PreprocessRelationship", back_populates = "preprocessed_articles")