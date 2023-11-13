from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

from routers.news_scraper import index as news
from models import news_article
from database.conn import engine, SessionLocal

app = FastAPI()
news_article.Base.metadata.create_all(bind = engine)

@app.get("/")
def say_hello():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}

app.include_router(news.router, prefix="/news")

print(f'Documents: http://localhost:8000/docs')