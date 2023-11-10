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

def is_exist_table(connection, table_name):
	# SQL 쿼리
	sql_query = f"SHOW TABLES LIKE '{table_name}'"

	result = connection.execute(sql_query)
	if result.fetchone():
			print(f"{table_name} 테이블이 존재합니다.")
			return 1
	else: 
			print(f"{table_name} 테이블이 존재하지 않습니다.")
			return 0
 
def create_raw_news_data(meta):
	Table(
		'raw_news_data', meta,
		Column('id', Integer, primary_key=True, autoincrement=True),
		Column('scraping_time', DateTime),
		Column('article_category', String(10)),
		Column('article_uploadtime', DateTime),
		Column('article_title', String(50)), 
		Column('article_content', String(255))
	)

class CRUD:
	#클래스 인스턴스 없이 메소드 호출 가능
	@staticmethod
	def insert(engine, table_name, connection, article_list):
		# with connection as conn:
		# 	conn.execute(insert(table),article_list)
		# 	conn.commit()
		db = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
		query = db.insert(table_name)
		result_proxy = connection.execute(query, article_list)
		result_proxy.close()
		# query = db.insert().values(scraping_time = scraping_time, article_category=category,article_uploadtime=upload_time,article_title=title,article_content=content)
		
		# begin() : 따로 commit을 수행하지 않아도 된다
		# with engine.begin() as conn:
		# 	conn.execute(query)
