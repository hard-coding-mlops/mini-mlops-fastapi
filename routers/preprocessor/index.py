from fastapi import APIRouter, HTTPException, status
import traceback
import re
from fastapi.responses import StreamingResponse
import json

from models.news_article import NewsArticle
from models.preprocessed_article import PreprocessedArticle
from database.conn import db_dependency
from .category_label import category_label

from routers import news_scraper

router = APIRouter()
# tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1', sp_model_kwargs={'nbest_size': -1, 'alpha': 0.6, 'enable_sampling': True})


async def preprocess_articles_full_progress(db: db_dependency):
    async def calculate_progress(total, current, start_percentage, end_percentage):
        return start_percentage + (current / total * (end_percentage - start_percentage))

    async def send_progress(kind, current, total, start_percentage, end_percentage):
        progress = await calculate_progress(total, current, start_percentage, end_percentage)
        data = {
            'kind': kind,
            'progress': progress,
        }
        yield f"data: {json.dumps(data)}\n\n"

    data = {
        'kind': "정제 시작",
        'progress': 1,
    }
    yield f"data: {json.dumps(data)}\n\n"
    
    last_scraped_order = (
        db.query(NewsArticle.scraped_order_no)
        .order_by(NewsArticle.scraped_order_no.desc())
        .limit(1)
        .first()
    )[0]
    last_scraped_news_articles = (
        db.query(NewsArticle)
        .filter(NewsArticle.scraped_order_no == last_scraped_order)
        .all()
    )
    
    print(f"\n\033[36m[Mini MLOps] \033[32m데이터 정제를 시작합니다.")
    
    non_duplicated_contents = set()
    non_duplicated_articles = []
    
    total_articles = len(last_scraped_news_articles)
    for index, article in enumerate(last_scraped_news_articles):
        for progress_data in send_progress("중복 제거", index, total_articles, 5, 25):
            yield progress_data
        
        if article.content not in non_duplicated_contents:
            non_duplicated_contents.add(article.content)
            non_duplicated_articles.append(article)
    
    total_non_duplicated_articles = len(non_duplicated_articles)
    for index, article in enumerate(non_duplicated_articles):
        for progress_data in send_progress("한글 이외 제거 + db 저장", index, total_non_duplicated_articles, 25, 75):
            yield progress_data
        
        preprocessed_article = PreprocessedArticle()
        article.title = re.sub('[^가-힣 ]', '', article.title).strip()
        article.content = re.sub('[^가-힣 ]', '', article.content).strip()
        length_of_content = len(article.content)
        
        if length_of_content > 10:
            formatted_text = article.title + article.content
            preprocessed_article.category_no = category_label[article.category]
            preprocessed_article.formatted_text = formatted_text
            preprocessed_article.original_article_id = article.id
            db.add(preprocessed_article)
            db.commit()
            db.refresh(preprocessed_article)
    
    data = {
        'kind': "정제 완료",
        'progress': 100,
    }
    yield f"data: {json.dumps(data)}\n\n"
    
    print(f"\n\033[36m[Mini MLOps] \033[32m데이터 정제가 완료되었습니다.")




def preprocess_articles(db: db_dependency):
    # news_scraper.index.scrape_news_articles(db)
    
    data = {
        'kind': "정제 시작",
        'progress': 51,
    }
    yield f"data: {json.dumps(data)}\n\n"
    last_scraped_order = (
        db.query(NewsArticle.scraped_order_no)
        .order_by(NewsArticle.scraped_order_no.desc())
        .limit(1)
        .first()
    )[0]
    last_scraped_news_articles = (
        db.query(NewsArticle)
        .filter(NewsArticle.scraped_order_no == last_scraped_order)
        .all()
    )
    
    print(f"\n\033[36m[Mini MLOps] \033[32m데이터 정제를 시작합니다.")
    
    non_duplicated_contents = set()
    non_duplicated_articles = []
    
    data = {
        'kind': "중복 제거",
        'progress': 55,
    }
    yield f"data: {json.dumps(data)}\n\n"
    # 중복 제거
    for article in last_scraped_news_articles:
        if article.content not in non_duplicated_contents:
            non_duplicated_contents.add(article.content)
            non_duplicated_articles.append(article)
    
    data = {
        'kind': "한글 이외 제거",
        'progress': 60,
    }
    yield f"data: {json.dumps(data)}\n\n"
    # 한글 이외 단어들 제거
    count = 0
    length_of_content = len(non_duplicated_articles)
    preprocessed_articles_length = 0
    for article in non_duplicated_articles:
        count += 1
        preprocessed_article = PreprocessedArticle()
        article.title = re.sub('[^가-힣 ]', '', article.title).strip()
        article.content = re.sub('[^가-힣 ]', '', article.content).strip()

        # 로딩 값 표시 61 ~ 99
        data = {
            'kind': "정제 데이터베이스 저장",
            'progress': 61 + (count / length_of_content) * 38,
        }
        yield f"data: {json.dumps(data)}\n\n"
        
        if length_of_content > 10:
            preprocessed_articles_length += 1
            formatted_text = article.title + article.content
            preprocessed_article.category_no = category_label[article.category]
            preprocessed_article.formatted_text = formatted_text
            preprocessed_article.original_article_id = article.id
            db.add(preprocessed_article)
            db.commit()
            db.refresh(preprocessed_article)
    
    print(f"\n\033[36m[Mini MLOps] \033[32m데이터 정제가 완료되었습니다.")
        
    data = {
        'kind': "정제 완료",
        'progress': 100,
        "length": preprocessed_articles_length,
    }
    yield f"data: {json.dumps(data)}\n\n"

@router.get("/preprocess", status_code=status.HTTP_200_OK)
def preprocess_articles_sse(db: db_dependency):
    return StreamingResponse(preprocess_articles(db), media_type="text/event-stream")
