import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

database_url = os.getenv("DATABASE_URL")
database_username = os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")
DB = f"mysql+pymysql://{database_username}:{database_password}@{database_url}"

# DB엔진 생성
engine = create_engine(DB, encoding = "utf-8")

# 데이터베이스 세션 클래스 -> 이를 이용해 생성한 인스턴스가 실제 데이터베이스 세션이 됨
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# DB모델이나 클래스를 만들기 위해 선언한 클래스 (추후 상속하여 사용)
Base = declarative_base()