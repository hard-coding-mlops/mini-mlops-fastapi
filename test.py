import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,MetaData,Table, Column, Integer, String, DateTime, insert
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

localhost = os.getenv("LOCALHOST") 
username = os.getenv("USERNAME") 
password = os.getenv("PASSWORD") 
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

DB = f"mysql+pymysql://{username}:{password}@{localhost}:{port}/{database_name}?charset=utf8"

engine = create_engine(DB, pool_recycle = 500)
connection = engine.connect()

session_maker = sessionmaker(bind=engine)
session = session_maker()

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

for k,v in Base.metadata.tables.items():
	print(f"{k}: {v}")
      
print(Base.metadata.tables)

Base.metadata.create_all(engine)

article=Article(current_time = "2023-01-01",
				category = "history",
				upload_time = "2023-01-01",
				title = "title",
        content = "content")

session.add(article)
session.commit()
session.delete(article)
session.commit()
session.close()