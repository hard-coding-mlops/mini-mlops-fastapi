import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

localhost = os.getenv("DATABASE_URL") 
username = os.getenv("DATABASE_USERNAME") 
password = os.getenv("DATABASE_PASSWORD") 
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

#column : 중복 여부를 수행할 행
def delete_duplicates(connection, table_name, column):
	sql_query = f"delete a from '{table_name}' a, '{table_name}' b where a.id > b.id and a.'{column}' = b.'{column}'"
	connection.execute(sql_query)

def remove_empty(connection, table_name, column):
	sql_query = f"delete from '{table_name}' where '{column}' =''"
	connection.execute(sql_query)
	