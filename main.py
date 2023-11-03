from typing import Union
from fastapi import FastAPI, HTTPException

from news_scraper.news_scraper import NewsScraper

app = FastAPI()

# python==3.11.5
# pip==23.2.1
# pip install -r requirements.txt
# uvicorn main:app --reload

@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

# @app.get("/news")
# def read_root():
#     print('start')
#     getNews()
#     return {"status": "success", "message": "뉴스 스크래핑을 완료했습니다."}

@app.get("/news")
def read_news():
    try:
        print('\n- [Mini MLOps] 뉴스 스크래핑을 시작합니다.')
        scraper = NewsScraper()
        scraper.scrape_news()
        scraper.save_data_to_csv()
        scraper.cleanup()
        print('- [Mini MLOps] 뉴스 스크래핑을 마칩니다.\n')
        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

