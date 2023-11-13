# python==3.11.5
# pip==23.2.1
# pip install -r requirements.txt
# uvicorn main:app --reload

from typing import Union
from fastapi import FastAPI, HTTPException, status
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

from fastapi import FastAPI
from routers import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

@app.get("/news")
def scrape_news():
    try:
        print('\n- [Mini MLOps]', end = ' ')
        news_scraper = NewsScraper()
        results = news_scraper.run()
        # for articles in results:
        #     for article in articles:
        
        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
