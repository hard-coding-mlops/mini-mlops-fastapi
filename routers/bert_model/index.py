from fastapi import APIRouter, HTTPException, status, Query
from .KoBert import bert_learn
from database.conn import db_dependency

router = APIRouter()

@router.get("/learn/{id}", status_code = status.HTTP_200_OK)
async def learn(db: db_dependency, id: int):
    result = await bert_learn(db, id)
    print(result)
    return {
        "status": "success",
        "message": "[Mini MLOps] GET /model/learn 완료되었습니다.",
        "data": result['formatted_text']
    }
