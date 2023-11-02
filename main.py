from typing import Union
from fastapi import FastAPI

from news_scraper.news_scraper import getNews

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "[Mini MLOps] Hello world from FastAPI."}
