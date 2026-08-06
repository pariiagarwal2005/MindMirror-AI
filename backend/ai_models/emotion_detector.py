from transformers import pipeline


emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)


def detect_emotion(text):

    result = emotion_model(text)

    return {
        "emotion": result[0]["label"],
        "confidence": result[0]["score"]
    }