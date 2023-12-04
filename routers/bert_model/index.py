from fastapi import APIRouter, HTTPException, status, Query
#from .KoBert import bert_learn
from models.preprocessed_article import PreprocessedArticle
from database.conn import db_dependency

router = APIRouter()

def add_embeddinglist_to_preprocessed_article(db: db_dependency, embedding_list):
    return 0

# @router.get("/learn/{id}", status_code = status.HTTP_200_OK)
# async def learn(db: db_dependency, id: int):
#     result = await bert_learn(db, id)
#     print(result)
#     return {
#         "status": "success",
#         "message": "[Mini MLOps] GET /model/learn 완료되었습니다.",
#         "data": result['formatted_text']
#     }
