from fastapi import APIRouter, HTTPException, status, Query
from .KoBert import bert_learn

router = APIRouter()

@router.get("/learn", status_code = status.HTTP_200_OK)
async def learn():
    bert_learn()
    return {
        "status": "success",
        "message": "[Mini MLOps] GET /model/learn 완료되었습니다.",
    }