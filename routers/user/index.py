from fastapi import APIRouter, HTTPException, status, Request
from httpx import AsyncClient
import traceback
from datetime import datetime
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from starlette.config import Config

from database.conn import db_dependency

router = APIRouter()

config = Config(".env")
KAKAO_REST_API_KEY = config("KAKAO_REST_API_KEY")
KAKAO_REDIRECT_URI = config("KAKAO_REDIRECT_URI")

class KakaoTokenRequest(BaseModel):
    code: str
    
@router.post("/kakao/login", status_code=status.HTTP_200_OK)
async def kakao_login(db: db_dependency, kakao_request: KakaoTokenRequest):
  try:
    print(kakao_request.code)
    print(KAKAO_REST_API_KEY)
    print(KAKAO_REDIRECT_URI)
    token_response = await AsyncClient().post(
      "https://kauth.kakao.com/oauth/token",
      params={
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": kakao_request.code,
        }
      )
    
    token_response.raise_for_status()
    access_token = token_response.json().get("access_token")
    
    user_response = await AsyncClient().get(
      'https://kapi.kakao.com/v2/user/me',
      headers={"Authorization": f"Bearer {access_token}"}
      )
    
    user_response.raise_for_status()
    user_info = user_response.json()
    
    return {"accessToken": access_token, "userInfo": user_info}
  
  except Exception as e:
    print(traceback.format_exc())
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e),
    )