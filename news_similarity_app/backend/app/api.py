from fastapi import APIRouter, HTTPException
from .schemas import URLRequest
from . import database, model
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.post("/analyze")
def analyze_news(data: URLRequest, db: Session = Depends(database.get_db)):
    try:
        print("[DEBUG] 요청 URL:", data.url)
        title, body, publisher = model.extract_article(data.url)
        print("[DEBUG] 기사 추출 성공:", title, "|", publisher)

        result = model.summarize_article(title, body)  # ✅ 변경된 부분

        # leaderboard.update_leaderboard(db, publisher, result["similarity"])  # ⛔ 미구현이라 주석

        print("[DEBUG] 요약 및 유사도 계산 성공:", result)

        return {
            "title": title,
            "body": body,
            "summary": result["summary"],
            "similarity_score": result["similarity"],
            "label": result["label"],  # ⬅️ 이거 추가!
            "threshold": result["threshold"],  # (optional) 기준값
            "publisher": publisher
        }

    except Exception as e:
        print("🔥 [ERROR] 분석 중 에러 발생!")
        print("🔥 에러 내용:", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leaderboard")
def leaderboard_api(db: Session = Depends(database.get_db)):
    # 구현 전이라 임시 빈 리스트 반환
    return []
