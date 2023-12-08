from fastapi import APIRouter, Request, HTTPException, status, Query
from database.conn import db_dependency,session
from pydantic import BaseModel
import torch
import os

from .train import call_model
from .graph import acc_loss_graph

from models.model import Model
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

@router.post("/learn", status_code=status.HTTP_200_OK)
def learn(db: db_dependency, params: Parameters):
    print('[MINI MLOps] /model/learn Start')
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
    
    # result_config = call_model(config)
    # print(result_config)
    call_model(config)

    return {
        "status": "success",
        "message": "[Mini MLOps] GET /model/learn 완료되었습니다.",
    }

@router.get("/hypra/{model_id}", status_code=status.HTTP_200_OK)
def hyperprameter(model_id:int):
    print("파라미터:", model_id)
    model_name = session.query(Model.model_name).filter(Model.model_id == model_id).first()
    model_path = f"/content/drive/MyDrive/mini_mlops_fastapi/learned_models/{model_name[0]}.pth"
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')  
    model = torch.load(model_path, map_location=device)

    graph = session.query(Graph.acc_graph, Graph.loss_graph, Graph.confusion_graph).filter(Graph.model_id == model_id).first()
    print(graph[0])
    
    return {
        'model_fn': model['config']['model_fn'],
        'max_len' : model['config']['max_len'],
        'batch_size' : model['config']['batch_size'],
        'num_epochs' : model['config']['num_epochs'],
        'warmup_ratio' : model['config']['warmup_ratio'],
        'max_grad_norm' : model['config']['max_grad_norm'],
        'learning_rate' : model['config']['learning_rate'],
        'split_rate' : model['config']['split_rate'],
        'data_num' : model['config']['data_num'],
        'acc' : model['config']['acc'],
        'loss' : model['config']['loss'],
        'accuracy' : model['config']['accuracy'],
        'precision' : model['config']['precision'],
        'recall' : model['config']['recall'],
        'f1' : model['config']['f1'],
        'acc_graph' : graph[0],
        'loss_graph' : graph[1],
        'confusion_graph' : graph[2]
    }
    
@router.get("/modellist", status_code = status.HTTP_200_OK)
def model_list(
    db:db_dependency,
    skip: int = Query(0, description="Skip the first N items", ge=0),
    limit: int = Query(12, description="Limit the number of items returned", le=100)
):
    print("modellist Start")
    file_path = '/content/drive/MyDrive/mini_mlops_fastapi/learned_models/'
    file_list = os.listdir(file_path)
    
    total_data = []
    
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')  
    for file in file_list:
        model_path = file_path + file
        model = torch.load(model_path , map_location=device)
        name = model['config']['model_fn'][:-4]
        acc = model['config']['acc']
        loss = model['config']['loss']
        max_len = model['config']['max_len']
        batch_size = model['config']['batch_size']
        num_epochs = model['config']['num_epochs']
        date = (
            db.query(Model.created_at)
            .filter(Model.model_name == name)
            .all()
        )
        
        data = {
            "model_name": name, 
            "acc": acc,
            "loss": loss,
            "max_len": max_len,
            "batch_size": batch_size,
            "num_epochs": num_epochs,
            "model_date": date[0][0]
        }
        
        total_data.append(data)
    paginated_data = total_data[skip : skip + limit]
    print("modellist End")
    return {
        "status": "success",
        "message": "[Mini MLOps] GET /data_management/all-data 완료되었습니다.",
        "total_ordered_data": paginated_data,
    }
    
@router.get("/topfive", status_code = status.HTTP_200_OK)
def acc_top_five():
    file_path = '/content/drive/MyDrive/mini_mlops_fastapi/learned_models/'
    file_list = os.listdir(file_path)
    
    total_data = []
    
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')  
    for file in file_list:
        model_path = file_path + file
        model = torch.load(model_path , map_location=device)
        name = model['config']['model_fn'][:-4]
        acc = model['config']['acc']
        loss = model['config']['loss']
        
        data = {
            "model_name": name,
            "acc": acc,
            "loss": loss
        }

        total_data.append(data)
        
    top_five = sorted(total_data, key=lambda x: x['acc'], reverse=True)
    
    return top_five[:5]