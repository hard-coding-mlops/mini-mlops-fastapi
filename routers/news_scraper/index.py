from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from models.news_article import NewsArticle
from models.scraped_order import ScrapedOrder
from database.conn import db_dependency
from .news_scraper import NewsScraper
from .format_time import get_formatted_current_date

router = APIRouter()

def save_news_article_and_scraped_order(db: Session, article_data, current_order_no):
    article_instance = NewsArticle(**article_data)
    db.add(article_instance)
    db.commit()
    db.refresh(article_instance)

    current_scraped_order = ScrapedOrder()
    current_scraped_order.news_article_id = article_instance.id
    current_scraped_order.scraped_order_no = current_order_no
    current_scraped_order.created_at = get_formatted_current_date()
    db.add(current_scraped_order)
    db.commit()
    db.refresh(current_scraped_order)

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_news_articles(db: db_dependency):
    news_articles = db.query(NewsArticle).all()
    return {"data": news_articles, "message": "[Mini MLOps] 뉴스 기사를 불러왔습니다."}

@router.get("/first-scrape", status_code=status.HTTP_200_OK)
async def first_scrape_news_articles(db: db_dependency):
    try:
        print("\n\033[36m[Mini MLOps] \033[37m", end=' ')

        news_scraper = NewsScraper()
        results = news_scraper.first_run()
        print("\n\033[36m[Mini MLOps] \033[32m뉴스 스크래핑을 마치고 데이터베이스에 저장합니다.\n이 작업은 꽤 걸립니다.")

        current_order_no = 1

        for articles in results:
            for article in articles:
                save_news_article_and_scraped_order(db, article, current_order_no)

        return {"status": "success", "message": "[Mini MLOps] 첫 뉴스 스크래핑을 완료했습니다."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scrape", status_code=status.HTTP_200_OK)
async def scrape_news_articles(db: db_dependency):
    try:
        print("\n\033[36m[Mini MLOps] \033[37m", end=' ')

        news_scraper = NewsScraper()
        results = news_scraper.run()
        print("\n\033[36m[Mini MLOps] \033[32m뉴스 스크래핑을 마치고 데이터베이스에 저장합니다.")
        print("\033[36m[Mini MLOps] \033[33m이 작업은 꽤 걸립니다.\n")

        last_scraped_order = db.query(ScrapedOrder).order_by(ScrapedOrder.id.desc()).first()
        current_order_no = last_scraped_order.scraped_order_no + 1 if last_scraped_order else 1

        for articles in results:
            for article in articles:
                save_news_article_and_scraped_order(db, article, current_order_no)

        return {"status": "success", "message": "[Mini MLOps] 뉴스 스크래핑을 완료했습니다.\n"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
