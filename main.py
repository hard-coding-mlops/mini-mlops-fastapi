from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

from routers.news_scraper import index as news
from models import news_article
from database.conn import engine, SessionLocal

app = FastAPI()
news_article.Base.metadata.create_all(bind = engine)

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

app.include_router(news.router, prefix="/news")

print(f'Documents: http://localhost:8000/docs')