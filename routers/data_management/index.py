from fastapi import APIRouter, HTTPException, status, Query
import traceback
import pandas as pd
import re
from kobert_tokenizer import KoBERTTokenizer
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func

from models.news_article import NewsArticle
from models.scraped_order import ScrapedOrder
from models.preprocessed_article import PreprocessedArticle
from database.conn import db_dependency

router = APIRouter()
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1', sp_model_kwargs={'nbest_size': -1, 'alpha': 0.6, 'enable_sampling': True})

@router.get("/total-ordered-data", status_code=status.HTTP_200_OK)
async def read_all(
    db: db_dependency,
    skip: int = Query(0, description="Skip the first N items", ge=0),
    limit: int = Query(12, description="Limit the number of items returned", le=100),
):
    total_ordered_data = []

    total_scraped_orders = db.query(ScrapedOrder.id, ScrapedOrder.start_datetime, ScrapedOrder.end_datetime).all()

    for order_id, start_datetime, end_datetime in total_scraped_orders:
        preprocessed_articles_count = (
            db.query(func.count(PreprocessedArticle.id))
            .join(NewsArticle, PreprocessedArticle.original_article_id == NewsArticle.id)
            .filter(NewsArticle.scraped_order_no == order_id)
            .scalar()
        )

        ordered_data = {
            "scraped_order_no": order_id,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "preprocessed_articles_length": preprocessed_articles_count,
        }

        total_ordered_data.append(ordered_data)

    paginated_data = total_ordered_data[skip : skip + limit]

    return {
        "status": "success",
        "message": "[Mini MLOps] GET data_management/all-data 완료되었습니다.",
        "data": paginated_data,
    }

@router.get("/single-preprocessed-data", status_code = status.HTTP_200_OK)
async def read_single(db: db_dependency):
    last_scraped_order = (
        db.query(ScrapedOrder.id)
        .order_by(ScrapedOrder.id.desc())
        .limit(1)
        .first()
    )[0]
    last_preprocessed_articles = (
            db.query(NewsArticle)
            .options(joinedload(NewsArticle.preprocessed_articles))
            .filter(NewsArticle.scraped_order_no == last_scraped_order, NewsArticle.preprocessed_articles != None)
            .all()
        )
    
    start_datetime = last_preprocessed_articles[0].upload_datetime
    end_datetime = last_preprocessed_articles[len(last_preprocessed_articles) - 1].upload_datetime
        
    return {
        "status": "success",
        "message": "[Mini MLOps] GET data_management/all-data 완료되었습니다.",
        "length": len(last_preprocessed_articles),
        "start_datetime":start_datetime,
        "end_datetime":end_datetime,
        "data": last_preprocessed_articles
    }
