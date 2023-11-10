# python==3.11.5
# pip==23.2.1
# pip install -r requirements.txt
# uvicorn main:app --reload

from typing import Union
from fastapi import FastAPI, HTTPException
import traceback
import os
from dotenv import load_dotenv

from news_scraper.news_scraper import NewsScraper
from news_article import NewsArticle
from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

engine = create_engine(DB_URL, pool_recycle = 500)
connection = engine.connect()

@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

@app.get("/news")
def read_news():
    try:
        print('\n- [Mini MLOps]', end = ' ')
        news_scraper = NewsScraper()
        news_scraper.run()
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        
        # for articles in results:
        #     for article in articles:
        #         session.add(article)
        #         session.commit()
        # session.close()
        
        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
