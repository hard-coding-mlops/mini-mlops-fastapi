import os
from dotenv import load_dotenv
from sqlalchemy import select, delete

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

localhost = os.getenv("DATABASE_URL") 
username = os.getenv("DATABASE_USERNAME") 
password = os.getenv("DATABASE_PASSWORD") 
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

DB = f"mysql+pymysql://{username}:{password}@{localhost}:{port}/{database_name}?charset=utf8"

# 테이블 존재 여부
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

# 중복 기사 제거 
def remove_duplicates(connection, table_name, column):
	# 내용이 같으면서 나중에 들어온 행 제거
	sql_query = f"delete a from {table_name} a, {table_name} b where a.id > b.id and a.{column} = b.{column}"
	connection.execute(sql_query)

# 빈 기사 제거
def remove_empty(connection, table_name, column):
	# 공백 지우고 문자열이 20이하인 행 제거 ex) 대구, 제보는 카카오톡 등
	sql_query = f"delete from {table_name} where length(REPLACE({column}, ' ','')) < 20"
	connection.execute(sql_query)

# 영어,기호 제거
def remove_without_korean(connection, table_name, column):
	# 한글이 아니면 공백으로 대체체
	sql_query = f"update {table_name} set {column} = REGEXP_REPLACE({column}, '[^가-힣]', ' ')"
	connection.execute(sql_query)