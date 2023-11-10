
# python==3.11.5
# pip==23.2.1
# pip install -r requirements.txt
# uvicorn main:app --reload

from typing import Union
from fastapi import FastAPI, HTTPException
import traceback
import os
from dotenv import load_dotenv
import numpy as np

from news_scraper.news_scraper import NewsScraper
from database import *
from news_article import *
from sqlalchemy import MetaData

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
            meta = MetaData() 
            create_raw_news_data(meta)
            meta.create_all(engine)

        newscraper = NewsScraper()
        results = newscraper.run()

        #session = engine.session_maker()
        # for articles in results:
        #     for article in articles:
        #         session.add(article)
        #article_list = np.array(results).flatten()

        # connection.execute(insert("raw_news_data"),article_list)
        # connection.commit()
        db = Table("raw_news_data", MetaData(), autoload=True, autoload_with=engine)
        query = db.insert("raw_news_data")
        for articles in results:
            for article in articles:
                #print(article.shape)
                print(article)
                result_proxy = connection.execute(query, article)
        result_proxy.close()
		
		
        #CRUD.insert(engine, "raw_news_data", connection, article_list)

        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) 

#
@app.get("/save-to-db")
def save_news_in_db():
    # Base.metadata.create_all(bind=engine)

    return {"status": "success", "message": "[Mini MLOps] 뉴스를 DB에 저장했습니다."}