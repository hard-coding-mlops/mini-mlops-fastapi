from fastapi import APIRouter, HTTPException, status
import traceback
import pandas as pd

from models.news_article import NewsArticle
from models.scraped_order import ScrapedOrder
from models.preprocessed_article import PreprocessedArticle
from database.conn import db_dependency

router = APIRouter()

# id, category 외래키
# category_NO, text, token_to_ids 테이블 생성
@router.get("/get", status_code = status.HTTP_200_OK)
async def read_all_news_articles(db: db_dependency):
    last_scraped_order = db.query(ScrapedOrder).order_by(ScrapedOrder.id.desc()).limit(1).first()
    last_scraped_news_articles = (
            db.query(NewsArticle)
            .join(ScrapedOrder)
            .filter(ScrapedOrder.scraped_order_no == last_scraped_order.scraped_order_no)
            .all()
        )
    
    news_article_df = pd.DataFrame([
        {
            "category": article.category,
            "title": article.title,
            "content": article.content,
        }
        for article in last_scraped_news_articles
    ])
    
    return {
        "status": "success",
        "message": "[Mini MLOps] 뉴스 기사를 불러왔습니다.",
        "length": len(last_scraped_news_articles),
        "data": last_scraped_news_articles,
    }

@router.get("/save-wanted-articles", status_code = status.HTTP_200_OK)
async def read_all_news_articles(db: db_dependency):
    last_scraped_order = db.query(ScrapedOrder).order_by(ScrapedOrder.id.desc()).limit(1).first()
    last_scraped_news_articles = (
            db.query(NewsArticle)
            .join(ScrapedOrder)
            .filter(ScrapedOrder.scraped_order_no == last_scraped_order.scraped_order_no)
            .all()
        )
    
    non_duplicated_contents = set()
    non_duplicated_articles = []
    
    for article in last_scraped_news_articles:
        if article.content not in non_duplicated_contents:
            non_duplicated_contents.add(article.content)
            non_duplicated_articles.append(article)
       
    # 중복 제거된 뉴스 기사 배열 non_duplicated_articles 
    
    return {
        "status": "success",
        "message": "[Mini MLOps] 뉴스 기사를 불러왔습니다.",
        "length": len(non_duplicated_articles),
        "data": last_scraped_news_articles,
    }
