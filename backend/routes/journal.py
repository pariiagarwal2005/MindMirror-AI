from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Journal

from ai_models.emotion_detector import detect_emotion
from ai_models.reflection_generator import generate_reflection


router = APIRouter()


@router.post("/journal")
def create_journal(
    text: str,
    db: Session = Depends(get_db)
):

    # Step 1: Detect emotion
    emotion_result = detect_emotion(text)


    # Step 2: Generate AI reflection
    reflection = generate_reflection(
        text,
        emotion_result["emotion"]
    )


    # Step 3: Create database entry
    new_journal = Journal(

        text=text,

        emotion=emotion_result["emotion"],

        confidence=str(
            emotion_result["confidence"]
        ),

        ai_reflection=reflection
    )


    # Step 4: Save in database
    db.add(new_journal)

    db.commit()

    db.refresh(new_journal)


    return {

        "message": "Journal saved",

        "id": new_journal.id,

        "text": new_journal.text,

        "emotion": new_journal.emotion,

        "confidence": new_journal.confidence,

        "ai_reflection": new_journal.ai_reflection,

        "created_at": new_journal.created_at
    }