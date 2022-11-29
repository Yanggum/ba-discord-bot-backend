from urllib.request import Request

from fastapi import FastAPI
from apps.chat.router import chat_router
from apps.database import db_instance


app = FastAPI()

# 서버 시작시 db connect
@app.on_event("startup")
async def startup():
    await db_instance.connect()


# 서버 종료시 db disconnect
@app.on_event("shutdown")
async def shutdown():
    await db_instance.disconnect()


# fastapi middleware, request state 에 db connection 심기
@app.middleware("http")
async def state_insert(request: Request, call_next):
    request.state.db_conn = db_instance
    response = await call_next(request)
    return response


# 데이터 베이스 이니셜라이즈

# 레디스 이니셜라이즈

# 미들웨어 정의

# 라우터 정의
app.include_router(chat_router)
