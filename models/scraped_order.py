from sqlalchemy import  Date, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base

class ScrapedOrder(Base):
    __tablename__ = "scraped_orders"

    id = Column(Integer, primary_key = True, index = True)
    news_article_id = Column(Integer, ForeignKey("news_articles.id"))
    scraped_order_no = Column(Integer)
    created_at = Column(Date)
    
    news_articles = relationship("NewsArticle", back_populates = "scraped_orders")