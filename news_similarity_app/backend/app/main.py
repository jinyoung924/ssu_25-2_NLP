from fastapi import FastAPI
from . import api, models, database, scheduler
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 인스턴스 먼저 생성
app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=database.engine)

# API 라우터 등록
app.include_router(api.router)

# 스케줄러 시작
scheduler.start_scheduler()
