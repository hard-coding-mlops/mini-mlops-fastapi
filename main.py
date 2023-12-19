import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

from routers.user import index as user
from routers.news_scraper import index as scraper
from routers.preprocessor import index as preprocessor
from routers.bert_model import index as bert_model
from routers.news_classifier import index as classifier
from routers.data_management import index as data_management

from models import news_article, preprocessed_article
from database.conn import engine, SessionLocal

app = FastAPI()

# 미들웨어
# CORS 정책
origins = [
    "http://localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/")
def say_hello():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

# 관리자 인증
app.include_router(user.router, prefix="/user")

# WEB API
app.include_router(data_management.router, prefix="/data_management")

# 수집
app.include_router(scraper.router, prefix="/scraper")

# 전처리(정제)
app.include_router(preprocessor.router, prefix="/preprocessor")

# 학습
app.include_router(bert_model.router, prefix="/model")

# 배포

# 서비스
app.include_router(classifier.router, prefix="/classifier")

print(f'Documents: http://localhost:8000/docs')

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)