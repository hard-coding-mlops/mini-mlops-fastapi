from fastapi import APIRouter, HTTPException, status
import traceback

from models.news_article import NewsArticle
from database.conn import db_dependency
from .news_scraper import NewsScraper

router = APIRouter()

@router.get("/", status_code = status.HTTP_200_OK)
async def read_all_news_articles(db: db_dependency):
    news_articles = db.query(NewsArticle).all()
    return {"data": news_articles, "message": "[Mini MLOps] 뉴스 기사를 불러왔습니다."}

@router.get("/first-scrape", status_code = status.HTTP_200_OK)
async def first_scrape_news_articles(db: db_dependency):
    try:
        print('\n- [Mini MLOps]', end = ' ')
        news_scraper = NewsScraper()
        results = news_scraper.first_run()
        
        for articles in results:
            for article in articles:
                article_instance = NewsArticle(**article)
                db.add(article_instance)
                db.commit()
                db.refresh(article_instance)
        
        return {"status": "success", "message": "[Mini MLOps] 첫 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/scrape", status_code = status.HTTP_200_OK)
async def scrape_news_articles(db: db_dependency):
    try:
        print('\n- [Mini MLOps]', end = ' ')
        news_scraper = NewsScraper()
        results = news_scraper.run()
        
        for articles in results:
            for article in articles:
                article_instance = NewsArticle(**article)
                db.add(article_instance)
                db.commit()
                db.refresh(article_instance)
        
        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))