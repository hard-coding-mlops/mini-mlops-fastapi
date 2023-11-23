from fastapi import APIRouter, HTTPException, status
import traceback
import pandas as pd
import re
from kobert_tokenizer import KoBERTTokenizer
from sqlalchemy.orm import joinedload

from models.news_article import NewsArticle
from models.preprocessed_article import PreprocessedArticle
from database.conn import db_dependency

router = APIRouter()
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1', sp_model_kwargs={'nbest_size': -1, 'alpha': 0.6, 'enable_sampling': True})

@router.get("/all-data", status_code = status.HTTP_200_OK)
async def read_all(db: db_dependency):
    
    last_scraped_order = (
        db.query(NewsArticle.scraped_order_no)
        .order_by(NewsArticle.scraped_order_no.desc())
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


@router.get("/single-preprocessed-data", status_code = status.HTTP_200_OK)
async def read_single(db: db_dependency):
    
    last_scraped_order = (
        db.query(NewsArticle.scraped_order_no)
        .order_by(NewsArticle.scraped_order_no.desc())
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
