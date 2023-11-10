
# python==3.11.5
# pip==23.2.1
# pip install -r requirements.txt
# uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
import traceback
import numpy as np

from news_scraper.news_scraper import NewsScraper
from database import *
from news_article import *
from sqlalchemy.orm import declarative_base

app = FastAPI()

# DB 연결
engine = create_engine(DB, pool_recycle = 500)
connection = engine.connect()

@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

#DB 수집 
@app.get("/news")
def read_news():
    try:
        print('\n- [Mini MLOps]', end = ' ')
        
        if is_exist_table(connection, "raw_news_data") == 0:    
            Base.metadata.create_all(engine)
            
        newscraper = NewsScraper()
        results = newscraper.run()

        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        
        for articles in results:
            for article in articles:
                session.add(article)
                session.commit()
        session.close()

        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) 

#
@app.get("/save-to-db")
def save_news_in_db():
    # Base.metadata.create_all(bind=engine)

    return {"status": "success", "message": "[Mini MLOps] 뉴스를 DB에 저장했습니다."}