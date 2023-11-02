from typing import Union
from fastapi import FastAPI

from news_scraper.news_scraper import getNews

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

@app.get("/news")
def read_root():
    print('start')
    getNews()
    return {"status": "success", "message": "뉴스 스크래핑을 완료했습니다."}
