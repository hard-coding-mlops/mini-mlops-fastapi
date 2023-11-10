#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, declarative_base
from sqlalchemy import MetaData,Table, Column, Integer, String, DateTime,BIGINT
from sqlalchemy.schema import CreateTable 
from sqlalchemy.dialects import mysql
from database import *
from pydantic import BaseModel
#from __future__ import annotations

# engine = EngineConn()
# connection = engine.connection()

# #DB모델이나 클래스를 만들기 위해 선언한 클래스 (추후 상속하여 사용)
# # 상속클래스들을 자동으로 인지하고 알아서 매핑해줌.
# Base = declarative_base()
# metadata = MetaData()

Base = declarative_base()

class Article(Base):
	__tablename__ = 'raw_news_data'

	id = Column(Integer, autoincrement=True, primary_key=True)
	scraping_time = Column(DateTime)
	article_category = Column(String(10), nullable=False)
	article_uploadtime = Column(DateTime)
	article_title = Column(String(50), nullable=False)
	article_content = Column(String(255), nullable=False)

	def __init__(self, current_time, category, upload_time, title, content):
		self.scraping_time=current_time, 
		self.article_category=category, 
		self.article_uploadetime=upload_time, 
		self.article_title=title, 
		self.article_content=content

	def __repr__(self):
			return f"Article(id={self.id!r}, scraping_time={self.scraping_time!r}, article_category={self.article_category!r}), article_uploadtime={self.article_uploadtime!r}), article_title={self.article_title!r}), article_content={self.article_content!r})"

Base.metadata.create_all(engine)


	
	