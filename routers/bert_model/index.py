from fastapi import APIRouter
from database.conn import db_dependency, session
from pydantic import BaseModel

import torch
from .train import main

from models.graph import Graph
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
#@router.post("/save")
def save_graph(config):
    file_path = './image/'
    acc_image = f'{file_path}{config["model_fn"]}_acc.jpg';
    loss_image = f'{file_path}{config["model_fn"]}_loss.jpg';
    
    graph = Graph
    graph.acc_graph = acc_image
    graph.loss_graph = loss_image
    
    session.add(graph)
    session.commit()
    session.refresh(graph)
    