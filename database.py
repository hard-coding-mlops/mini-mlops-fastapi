import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_HOST = os.getenv("DATABASE_HOST")
DB_USERNAME = os.getenv("DATABASE_USERNAME")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
