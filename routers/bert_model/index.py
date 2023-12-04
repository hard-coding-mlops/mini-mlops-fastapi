from fastapi import APIRouter, Request, HTTPException, status, Query
from database.conn import db_dependency
from pydantic import BaseModel

import torch
from .train import main

from routers.data_management.index import preprocessed_articles

class Parameters(BaseModel):
    model_filename: str
    max_len: int
    batch_size: int
    num_epochs: int
    warmup_ratio: float
    max_grad_norm: int
    learning_rate: float
    split_rate: float
    data_length: int
    

router = APIRouter()

@router.post("/learn")
async def learn(db: db_dependency, params: Parameters):
    config = {
        'model_fn': f"{params.model_filename}.pth",
        'max_len' : params.max_len,
        'batch_size' :params.batch_size,
        'num_epochs' :params.num_epochs,
        'warmup_ratio' :params.warmup_ratio,
        'max_grad_norm' :params.max_grad_norm,
        'log_interval' : 200,
        'learning_rate' :params.learning_rate,
        'split_rate' :params.split_rate,
        'data_num' :params.data_length,
        "gpu_id": 0 if torch.cuda.is_available() else -1,
        'acc' : 0.0,
        'loss': 0.0,
        'accuracy' : 0.0,
        'precision' : 0.0,
        'recall' : 0.0,
        'f1' : 0.0
    }
    print(config)
    main(config)
    
    return {
        "status": "success",
        "message": "[Mini MLOps] GET /model/learn 완료되었습니다.",
    }
