from sqlalchemy.orm import Session
from . import models

def save_score(db: Session, publisher: str, score: float):
    db_score = models.Score(publisher=publisher, score=score)
    db.add(db_score)
    db.commit()