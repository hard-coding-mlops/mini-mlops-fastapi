from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

from routers.news_scraper import index as scraper
# from routers.preprocessor import index as preprocessor
from routers.news_classifier import index as classifier
from models import news_article, preprocessed_article, scraped_order
from database.conn import engine, SessionLocal

app = FastAPI()
news_article.Base.metadata.create_all(bind = engine)
# preprocessed_article.Base.metadata.create_all(bind = engine)
scraped_order.Base.metadata.create_all(bind = engine)


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

app.include_router(scraper.router, prefix="/scraper")
# app.include_router(preprocessor.router, prefix="/preprocessor")
app.include_router(classifier.router, prefix="/classifier")

print(f'Documents: http://localhost:8000/docs')