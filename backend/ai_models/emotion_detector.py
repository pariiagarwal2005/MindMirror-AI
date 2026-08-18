from transformers import pipeline


_emotion_model = None


def get_emotion_model():
    global _emotion_model

    if _emotion_model is None:
        print("Loading emotion model...")

        _emotion_model = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            device="mps"
        )

        print("Emotion model loaded.")

    return _emotion_model


def detect_emotion(text):
    model = get_emotion_model()

    result = model(text)

    return {
        "emotion": result[0]["label"],
        "confidence": result[0]["score"]
    }