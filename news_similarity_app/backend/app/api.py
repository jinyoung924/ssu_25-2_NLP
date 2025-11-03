from fastapi import APIRouter, HTTPException
from .schemas import URLRequest
from . import database, model, leaderboard
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.post("/analyze")
def analyze_news(data: URLRequest, db: Session = Depends(database.get_db)):
    try:
        title, body, publisher = model.extract_article(data.url)
        score, summary = model.get_similarity_and_summary(title, body)
        leaderboard.update_leaderboard(db, publisher, score)
        return {
            "title": title,
            "body": body,
            "summary": summary,
            "similarity_score": score,
            "publisher": publisher
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/leaderboard")
def leaderboard_api(db: Session = Depends(database.get_db)):
    return leaderboard.get_leaderboard(db)