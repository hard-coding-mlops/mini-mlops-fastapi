from fastapi import APIRouter, Request, HTTPException, status, Query
from database.conn import db_dependency,session
from sqlalchemy.sql import func
from sqlalchemy import desc
from pydantic import BaseModel
from datetime import datetime

from models.model import Model
from models.graph import Graph
from models.epoch import Epoch
from models.deployment import Deployment
from models.client import Client

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

# @router.post("/learn", status_code=status.HTTP_200_OK)
# async def learn(params: Parameters):
#     print("[MINI MLOps] /model/learn 시작")
#     data = {
#         'kind': "학습 시작",
#         'progress': 0
#     }
    
#     config = {
#         'model_fn': f"{params.model_filename}.pth",
#         'max_len' : params.max_len,
#         'batch_size' :params.batch_size,
#         'num_epochs' :params.num_epochs,
#         'warmup_ratio' :params.warmup_ratio,
#         'max_grad_norm' :params.max_grad_norm,
#         'log_interval' : 200,
#         'learning_rate' :params.learning_rate,
#         'split_rate' :params.split_rate,
#         'data_num' :params.data_length,
#         "gpu_id": 0 if torch.cuda.is_available() else -1,
#         'acc' : 0.0,
#         'loss': 0.0,
#         'accuracy' : 0.0,
#         'precision' : 0.0,
#         'recall' : 0.0,
#         'f1' : 0.0
#     }
#     yield f"data: {json.dumps(data)}\n\n"
#     #await call_model(config)
#     async for result_data in call_model(config):
#         yield f"{result_data}"
    
#     data = {
#         'kind': "학습 완료",
#         'progress': 100,
#         "acc" : config['acc'],
#         "loss" : config['loss']
#     }
#     yield f"data: {json.dumps(data)}\n\n"
    
#     print("[Mini MLOps] GET /data_management/model/list 완료되었습니다.")

    
# @router.post("/learn-progress", status_code = status.HTTP_200_OK)
# async def learn_progress(params: Parameters):
# 	return StreamingResponse(learn(params), media_type="text/event-stream")

# @router.get("/hypra/{model_id}", status_code=status.HTTP_200_OK)
# def hyperprameter(db:db_dependency, model_id:int):
#     print("파라미터:", model_id)
#     parameter = (
#         db.query(Model.model_name,
#                       Model.max_length,
#                       Model.batch_size,
#                       Model.num_epochs,
#                       Model.learning_rate,
#                       Model.warmup_ratio,
#                       Model.max_grad_norm,
#                       Model.split_rate,
#                       Model.data_length,
#                       Model.acc,
#                       Model.loss,
#                       Model.accuracy,
#                       Model.precision_value,
#                       Model.recall,
#                       Model.f1,
#                       Deployment.deployed_at,
#                       Graph.acc_graph,
#                       Graph.loss_graph,
#                       Graph.confusion_graph
#                       )
#         .join(Deployment.model_id == model_id and Graph.model_id == model_id)
#         .filter(Model.model_id == model_id)
#         .first()
#     )
    
#     return {
#         'model_fn': parameter[0],
#         'max_len' : parameter[1],
#         'batch_size' : parameter[2],
#         'num_epochs' : parameter[3],
#         'learning_rate' : parameter[4],
#         'warmup_ratio' : parameter[5],
#         'max_grad_norm' : parameter[6],
#         'split_rate' : parameter[7],
#         'data_length' : parameter[8],
#         'acc' : parameter[9],
#         'loss' : parameter[10],
#         'accuracy' : parameter[11],
#         'precision_value' : parameter[12],
#         'recall' : parameter[13],
#         'f1' : parameter[14],
#         'acc_graph' : parameter[15],
#         'loss_graph' : parameter[16],
#         'confusion_graph' : parameter[17]
#     }

# ---
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_models(
    db: db_dependency,
    skip: int = Query(0, description="Skip the first N items", ge=0),
    limit: int = Query(100, description="Limit the number of items returned", le=100),
):
    # db.execute("CREATE INDEX idx_model_id ON model (model_id);")

    total_models = (
        db.query(
            Model.model_id,
            Model.model_name,
            Model.created_at,
            Model.data_length,
            Model.num_epochs,
            Model.batch_size,
            Model.max_length,
            Model.acc,
            Model.loss,
        )
        .order_by(desc(Model.model_id))
        .offset(skip)
        .limit(limit)
        .all()
    )

    total_models = [
        {
            "model_id": model.model_id,
            "model_name": model.model_name,
            "created_at": model.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "data_length": model.data_length,
            "num_epochs": model.num_epochs,
            "batch_size": model.batch_size,
            "max_length": model.max_length,
            "acc": model.acc,
            "loss": model.loss,
        }
        for model in total_models
    ]

    return {
        "status": "success",
        "message": "[Mini MLOps] GET /data_management/model/list 완료되었습니다.",
        "length": len(total_models),
        "data": total_models,
    }

@router.get("/top-five", status_code = status.HTTP_200_OK)
async def top_five_models(db: db_dependency):
    top_five_models = (
        db.query(Model.model_id, Model.model_name, Model.acc, Model.loss)
        .order_by(Model.accuracy.desc())
        .limit(5)
        .all()
    )
    print(top_five_models)
    return {
        "status": "success",
        "message": "[Mini MLOps] GET /data_management/model/top 완료되었습니다.",
        "data" : [{"model_id": row[0], "model_name": row[1], "accuracy": row[2], "loss": row[3]} for row in top_five_models]
    }

def _current_active():
    model_id = (
        session.query(Deployment.model_id)
        .filter(Deployment.active == 1)
        .first()
    )
    print(model_id)
    return model_id[0]
    

@router.get("/currently-active", status_code = status.HTTP_200_OK)
async def active(db: db_dependency):
    model_id = _current_active()
    usage = db.query(func.count()).filter(Client.model_id == model_id).scalar() 
    model = db.query(Model.model_name, Model.acc, Model.loss).filter(Model.model_id == model_id).first()
    evaluation_equal = db.query(func.count()).filter(Client.predict_result == Client.client_result,Client.model_id == model_id).scalar()
    evaluation_diff = db.query(func.count()).filter(Client.predict_result != Client.client_result,Client.client_result != '-',Client.model_id == model_id).scalar()
    evaluation_noresponse = db.query(func.count()).filter(Client.client_result == '-',Client.model_id == model_id).scalar()
    
    return {
        "status": "success",
        "message": f"[Mini MLOps] GET /data_management/model/currently_active 완료되었습니다.",
        "usage": usage,
        "model_name" : model[0],
        "acc": model[1],
        "loss": model[2],
        "evaluation_equal": evaluation_equal,
        "evaluation_diff": evaluation_diff,
        "evaluation_noresponse": evaluation_noresponse
    }
    
@router.get("/deploy/{id}", status_code=status.HTTP_200_OK)
async def active(id: int):
    try:
        model_id = _current_active()
        print(model_id)
        
        old_model = session.query(Deployment).filter(Deployment.model_id == model_id).first()
        old_model.active = 0
        
        new_model = session.query(Deployment).filter(Deployment.model_id == id).first()
        new_model.deployed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_model.active = 1
        
        session.commit()
        print(new_model.model_name)

        return {
            "status": "success",
            "message": f"[Mini MLOps] GET /data_management/model/deploy/{id} 완료되었습니다."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"에러 발생: {str(e)}"
        }

def _save_client(model_id,insert,result):
    client = Client()
    client.model_id = model_id
    client.user_insert = insert
    client.predict_result = result  
        
    session.add(client)
    session.commit()
    session.refresh(client)
    
    return client.client_id

class Article(BaseModel):
    user_input: str

# @router.post("/classify", status_code = status.HTTP_200_OK)
# async def active(db: db_dependency, article:Article):
#     model_id = _current_active()
#     model = db.query(Model.model_name, Model.max_length, Model.batch_size).filter(Model.model_id == model_id).first()
    
#     config = {
#         'model_name' : model[0],
#         'max_len' : model[1],
#         'batch_size' :model[2]
#     }
    
#     result = predict(config,article.user_input)
    
#     client_id = _save_client(model_id,article.user_input,result)
    
#     return {
#         "status": "success",
#         "message": f"[Mini MLOps] GET /data_management/model/classify/{article.user_input} 완료되었습니다.",
#         "result" : result,
#         "client_id" : client_id
#     }

class Client_log(BaseModel):
    client_id : int
    reinput : str

@router.post("/evaluate", status_code = status.HTTP_200_OK)
async def active(client_log:Client_log):
    client = session.query(Client).filter(Client.client_id == client_log.client_id).first()
    print(client_log.reinput)
    client.client_result = client_log.reinput
    session.commit()
    
    return {
        "status": "success",
        "message": f"[Mini MLOps] GET /data_management/model/evaluate/{client_log.client_id}/{client_log.reinput} 완료되었습니다."
    }

@router.get("/clients", status_code = status.HTTP_200_OK)
async def read_all_clients(db: db_dependency,
    skip: int = Query(0, description="Skip the first N items", ge=0),
    limit: int = Query(100, description="Limit the number of items returned", le=100),
):
    
    total_clients = (
        db.query( 
            Client.client_id,
            Client.use_at,
            Model.model_name, 
            Client.predict_result,
            Model.acc, 
            Client.client_result
        )
        .join(Client)
        .filter(Model.model_id == Client.model_id)
        .order_by(Client.client_id.desc())
        .offset(skip)
        .limit(limit)
        .all() 
    )
    
    total_clients = [
        {
            "client_id" : client.client_id,
            "use_at": client.use_at,
            "model_name": client.model_name, 
            "predict_result": client.predict_result,
            "acc": client.acc, 
            "client_result": client.client_result
        }
        for client in total_clients
    ]
    
    return {
        "status": "success",
        "message": "[Mini MLOps] GET /data_management/clients 완료되었습니다.",
        "length": len(total_clients),
        "data": total_clients,
    }

    
@router.get("/clients/{client_id}", status_code = status.HTTP_200_OK)
async def read_all_clients(db: db_dependency, client_id: int):
    client = (
        db.query( 
            Client.use_at,
            Model.model_name, 
            Client.predict_result,
            Model.acc, 
            Client.client_result,
            Client.user_insert
        )
        .join(Client)
        .filter(Client.client_id == client_id, Model.model_id == Client.model_id)
        .first() 
    )
    
    return {
        "status": "success",
        "message": f"[Mini MLOps] GET /data_management/clients/{client_id} 완료되었습니다.",
        "use_at" : client[0],
        "model_name" : client[1],
        "predict_result" : client[2],
        "acc" : client[3],
        "client_result" : client[4],
        "user_insert" : client[5]
    }

# @router.get("/test/{model_id}", status_code = status.HTTP_200_OK)
# async def test(db: db_dependency, model_id:int):
#     quest = db.query(Test.quest).all()
#     model = db.query(Model.model_name, Model.max_length, Model.batch_size).filter(Model.model_id == model_id).first()
    
#     config = {
#         'model_name' : model[0],
#         'max_len' : model[1],
#         'batch_size' :model[2]
#     }
    
#     for i in range(len(quest)):
#         que = quest[i][0]
        
#         res = predict(config, que)
        
#         data = {
#             "answer" : res
#         }
#         yield f"data: {json.dumps(data)}\n\n"
    
#     # return { 
#     #     "status": "success",
#     #     "message": f"[Mini MLOps] GET /data_management/test 완료되었습니다.",
#     #     "quest_list" : quest_list,
#     #     "answer_list" : answer_list,
#     #     "predict_list" : predict_list,
#     #     "result_list" : result_list
#     # }

# @router.get("/test-progress/{model_id}", status_code = status.HTTP_200_OK)
# async def test_progress(db:db_dependency, model_id:int):
# 	return StreamingResponse(test(db,model_id), media_type="text/event-stream")

@router.get("/{id}", status_code = status.HTTP_200_OK)
async def read_all_epochs(db: db_dependency, id: int):
    model_found = db.query(Model).filter(Model.model_id == id).first()
    graph_found = db.query(Graph).filter(Graph.model_id == id).first()
    epoch_found = db.query(Epoch).filter(Epoch.model_id == id).order_by(Epoch.epoch_number).all()

    return {
        "status": "success",
        "message": f"[Mini MLOps] GET /data_management/model/{id} 완료되었습니다.",
        "model": model_found,
        "epoch": epoch_found,
        "graph": graph_found,
    }

# @router.get("/currently-active", status_code = status.HTTP_200_OK)
# async def current(db: db_dependency):
#     useage = db.query(Deployment).filter()
#     acc = 
    

#     return {
#         "status": "success",
#         "message": f"[Mini MLOps] GET /data_management/model/{id} 완료되었습니다.",
#         "model": model_found,
#         "epoch": epoch_found,
#         "graph": graph_found,
#     }
    
