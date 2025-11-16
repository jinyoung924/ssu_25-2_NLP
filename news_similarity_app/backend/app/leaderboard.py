from fastapi import APIRouter, HTTPException, Depends
from .schemas import URLRequest
from . import database, model, leaderboard
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/analyze")
def analyze_news(data: URLRequest, db: Session = Depends(database.get_db)):
    try:
        # URL에서 기사 추출
        title, body, publisher = model.extract_article(data.url)

        # 기사 요약 및 유사도 분석
        result = model.summarize_article(title, body)

        # 리더보드 업데이트
        leaderboard.update_leaderboard(db, publisher, result["similarity"])

        return {
            "title": title,
            "body": body[:300],
            "summary": result["summary"],
            "similarity_score": result["similarity"],
            "label": result["label"],
            "threshold": result["threshold"],
            "publisher": publisher
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leaderboard")
def leaderboard_api(db: Session = Depends(database.get_db)):
    return leaderboard.get_leaderboard(db)
