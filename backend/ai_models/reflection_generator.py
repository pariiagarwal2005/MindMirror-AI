def generate_reflection(text, emotion=None):
    """
    Generates a simple fallback reflection.

    NOTE:
    MindMirror's main conversational intelligence is now handled
    by the chat system. This function remains available for the
    journal/reflection feature.
    """

    text = text.strip()

    if not text:
        return (
            "I'm here. You can start wherever feels easiest."
        )

    lower_text = text.lower()

    # =========================================================
    # SAFETY
    # =========================================================

    serious_keywords = [
        "kill myself",
        "suicide",
        "end my life",
        "want to die",
        "don't want to live",
        "hurt myself",
        "self harm",
        "self-harm"
    ]

    if any(keyword in lower_text for keyword in serious_keywords):

        return (
            "🫂 I'm really sorry you're carrying something this heavy. "
            "I'm glad you said it instead of keeping it completely to "
            "yourself.\n\n"
            "Right now, your safety matters more than figuring everything "
            "else out. Please stay around someone you trust and reach out "
            "for immediate support if you feel you might act on these "
            "thoughts.\n\n"
            "Are you in immediate danger right now?"
        )

    # =========================================================
    # NATURAL FALLBACK
    # =========================================================

    return (
        f"💜 I hear you.\n\n"
        f"You said: \"{text}\"\n\n"
        "You don't have to explain everything perfectly. "
        "I'm here, and we can take this one thought at a time."
    )