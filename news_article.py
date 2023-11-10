from sqlalchemy import Column, Integer, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "RAW_NEWS"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    upload_datetime = Column(DateTime, nullable=False)
    category = Column(String(10), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text)

    def __init__(self, upload_datetime, category, title, content):
        self.category = category
        self.upload_datetime = upload_datetime
        self.title = title
        self.content = content
        
    # def __repr__(self):
    #     return f"Article(id={self.id!r}, scraping_time={self.scraping_time!r}, article_category={self.article_category!r}), article_uploadtime={self.article_uploadtime!r}), article_title={self.article_title!r}), article_content={self.article_content!r})"