from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Journal
from core.security import get_current_user

from ai_models.emotion_detector import detect_emotion
from ai_models.reflection_generator import generate_reflection


router = APIRouter()


@router.post("/journal")
def create_journal(
    text: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    emotion_result = detect_emotion(text)

    emotion = emotion_result["emotion"]

    confidence = emotion_result["confidence"]

    reflection = generate_reflection(
    text,
    emotion_result["emotion"]
    )

    new_journal = Journal(
        text=text,
        emotion=emotion,
        confidence=str(confidence),
        ai_reflection=reflection,
        user_id=current_user.id
    )

    db.add(new_journal)

    db.commit()

    db.refresh(new_journal)

    return {
        "message": "Journal saved",
        "id": new_journal.id,
        "text": new_journal.text,
        "user_id": new_journal.user_id,
        "emotion": new_journal.emotion,
        "confidence": new_journal.confidence,
        "ai_reflection": new_journal.ai_reflection,
        "created_at": new_journal.created_at
    }


@router.get("/journal/history")
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    journals = (
        db.query(Journal)
        .filter(
            Journal.user_id == current_user.id
        )
        .order_by(
            Journal.created_at.desc()
        )
        .all()
    )

    return journals