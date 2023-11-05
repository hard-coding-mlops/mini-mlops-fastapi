from typing import Union
from fastapi import FastAPI, HTTPException
import traceback

from news_scraper.news_scraper import NewsScraper

app = FastAPI()

# python==3.11.5
# pip==23.2.1
# pip install -r requirements.txt
# uvicorn main:app --reload
from datetime import datetime
import pytz
@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

@app.get("/news")
def read_news():
    try:
        print('\n- [Mini MLOps]', end = ' ')
        news_scraper = NewsScraper()
        news_scraper.run()
        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/save-to-db")
def save_news_in_db():
    try:
        print('\n- [Mini MLOps]', end = ' ')
        news_scraper = NewsScraper()
        news_scraper.save_news_in_db()
        return {"status": "success", "message": "[Mini MLOps] 뉴스를 DB에 저장했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))