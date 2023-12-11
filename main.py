import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

from routers.news_scraper import index as scraper
from routers.preprocessor import index as preprocessor
# from routers.bert_model import index as bert_model
from routers.news_classifier import index as classifier
from routers.data_management import index as data_management

from models import news_article, preprocessed_article
from database.conn import engine, SessionLocal

app = FastAPI()
news_article.Base.metadata.create_all(bind = engine)
preprocessed_article.Base.metadata.create_all(bind = engine)

# 미들웨어
# CORS 정책
origins = [
    "http://localhost:3000",
    "http://211.62.99.58:3000",
    "http://211.62.99.58:3010"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


temp = "TEMP"
@app.get("/")
def say_hello():
    print(temp)
    return {"temp": temp, "message": "[Mini MLOps] Hello world from FastAPI."}

@app.get("/test1")
def say_hello():
    temp = "TEMP - 1"
    print(temp)
    return {"temp": temp, "message": "[Mini MLOps] Hello world from FastAPI."}

@app.get("/test2")
def say_hello():
    temp = "TEMP - 2"
    print(temp)
    return {"temp": temp, "message": "[Mini MLOps] Hello world from FastAPI."}

# WEB API
app.include_router(data_management.router, prefix="/data_management")

# 수집
app.include_router(scraper.router, prefix="/scraper")

# 전처리(정제)
app.include_router(preprocessor.router, prefix="/preprocessor")

# 학습
# app.include_router(bert_model.router, prefix="/model")

# 배포

# 서비스
app.include_router(classifier.router, prefix="/classifier")

import time

app = FastAPI()

@app.get('/test')
def test_one():
    print("1111111 start")
    time.sleep(3)
    print("test_one is on process")
    time.sleep(5)
    print("ending 1111111")
    return {"message": "Done Test One"}


@app.get('/hello')
def hello_world():
    print("Hello World!")
    time.sleep(3)
    print("In the middle of the world.")
    time.sleep(5)
    print("Goodbye World.")
    return {"message": "Done Hello World"}

import os
from pyngrok import ngrok
import uvicorn

# Set the authtoken for the ngrok tunnel
os.environ["NGROK_AUTH_TOKEN"] = "2ZLuyiA0f6UNv5uKnapcZpqjo6Y_7wQJxgGfd2m85JHiB6JZ2"

# Set the port for the server
port = 8000

# Open an ngrok tunnel to the server
public_url = ngrok.connect(port)
print('Public URL:', public_url)

# Enable the 'eventlet' worker to support multiple connections
# uvicorn.run("main:app", host="127.0.0.1", port=port, workers=2)


print(f'Documents: http://localhost:8000/docs')

if __name__ == '__main__':
    # uvicorn.run("main:app", reload=True)
    uvicorn.run("main:app", host="127.0.0.1", port=port, workers=2)