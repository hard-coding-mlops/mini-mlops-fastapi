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

