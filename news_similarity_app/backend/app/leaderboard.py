from sqlalchemy.orm import Session
from collections import defaultdict
from . import models

def update_leaderboard(db: Session, publisher, score):
    db_score = models.Score(publisher=publisher, score=score)
    db.add(db_score)
    db.commit()

def get_leaderboard(db: Session):
    records = db.query(models.Score).all()
    pub_scores = defaultdict(list)
    for r in records:
        pub_scores[r.publisher].append(r.score)
    return [
        {"publisher": p, "avg_score": round(sum(v)/len(v), 4)}
        for p, v in pub_scores.items()
    ]