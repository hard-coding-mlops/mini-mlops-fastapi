import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,MetaData,Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

localhost = os.getenv("LOCALHOST") 
username = os.getenv("USERNAME") 
password = os.getenv("PASSWORD") 
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

DB = f"mysql+pymysql://{username}:{password}@{localhost}:{port}/{database_name}?charset=utf8" 

# DB엔진 생성
engine = create_engine(DB)

class engineconn:
    def __init__(self):
        self.engine = create_engine(DB, pool_recycle =500)

    def sessionmaker(self):
				# 데이터베이스 세션 클래스 -> 이를 이용해 생성한 인스턴스가 실제 데이터베이스 세션이 됨
        Session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

def is_exist_table(table_name):
	# SQL 쿼리
	sql_query = f"SHOW TABLES LIKE '{table_name}'"

	with engine.connect() as connection:
		result = connection.execute(sql_query)
		if result.fetchone():
				print(f"{table_name} 테이블이 존재합니다.")
				return 1
		else:
				print(f"{table_name} 테이블이 존재하지 않습니다.")
				return 0

def create_raw_news_data():
	meta = MetaData()

	raw_news_data = Table(
			'raw_news_data', meta,
			Column('id', Integer, primary_key=True, autoincrement=True),
			Column('scraping_time', DateTime),
			Column('article_category', String(10)),
			Column('article_uploadtime', DateTime),
			Column('article_title', String(50)),
			Column('article_content', String(255))
	)

	meta.create_all(engine)

class CRUD:
	#클래스 인스턴스 없이 메소드 호출 가능
	@staticmethod
	def insert(table_name, scraping_time, category,upload_time,title,content):
		db = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
		query = db.insert().values(scraping_time = scraping_time, article_category=category,article_uploadtime=upload_time,article_title=title,article_content=content)
		
		# begin() : 따로 commit을 수행하지 않아도 된다
		with engine.begin() as conn:
			conn.execute(query)

# DB모델이나 클래스를 만들기 위해 선언한 클래스 (추후 상속하여 사용)
Base = declarative_base()