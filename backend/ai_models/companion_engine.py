# =========================================================
# MINDMIRROR COMPANION ENGINE
# =========================================================


LISTEN = "listen"
COMFORT = "comfort"
ADVICE = "advice"
CELEBRATE = "celebrate"
EXPLAIN = "explain"
CASUAL = "casual"
SAFETY = "safety"
GENERAL = "general"


# =========================================================
# SAFETY DETECTION
# =========================================================

def contains_safety_signal(message):

    text = (
        message or ""
    ).strip().lower()


    safety_phrases = [

        "suicide",
        "suicidal",
        "suicidal thoughts",

        "kill myself",
        "killing myself",

        "end my life",
        "take my life",

        "want to die",
        "wanna die",

        "don't want to live",
        "dont want to live",
        "do not want to live",

        "hurt myself",
        "hurting myself",

        "harm myself",

        "self harm",
        "self-harm",
        "selfharm"

    ]


    return any(

        phrase in text

        for phrase in safety_phrases

    )


# =========================================================
# USER INDICATES CURRENT SAFETY
# =========================================================

def says_safe_now(message):

    text = (
        message or ""
    ).strip().lower()


    safe_phrases = [

        "i'm safe",
        "im safe",
        "i am safe",

        "i feel safe",

        "i'm okay now",
        "im okay now",
        "i am okay now",

        "i'm not going to hurt myself",
        "im not going to hurt myself",
        "i am not going to hurt myself",

        "i won't hurt myself",
        "i wont hurt myself",

        "i don't want to hurt myself",
        "i dont want to hurt myself"

    ]


    return any(

        phrase in text

        for phrase in safe_phrases

    )


# =========================================================
# DETECT MODE
# =========================================================

def detect_mode(message):

    text = (
        message or ""
    ).strip().lower()


    # -----------------------------------------------------
    # SAFETY ALWAYS HAS PRIORITY
    # -----------------------------------------------------

    if contains_safety_signal(
        message
    ):

        return SAFETY


    # -----------------------------------------------------
    # LISTEN
    # -----------------------------------------------------

    listen_phrases = [

        "just listen",

        "don't give advice",
        "dont give advice",

        "don't want advice",
        "dont want advice",

        "no advice",

        "just want someone to listen",

        "i just want to talk",

        "don't fix this",
        "dont fix this"

    ]


    if any(

        phrase in text

        for phrase in listen_phrases

    ):

        return LISTEN


    # -----------------------------------------------------
    # ADVICE
    # -----------------------------------------------------

    advice_phrases = [

        "what should i do",
        "what do i do",

        "what can i do",

        "how should i handle",
        "how do i handle",

        "what would you do",

        "give me advice",
        "need advice",

        "help me decide",

        "how can i fix",

        "tell me what to do"

    ]


    if any(

        phrase in text

        for phrase in advice_phrases

    ):

        return ADVICE


    # -----------------------------------------------------
    # CELEBRATE
    # -----------------------------------------------------

    celebration_phrases = [

        "got selected",
        "got accepted",

        "got the job",

        "i passed",

        "finally did it",

        "i won",

        "i achieved",

        "so excited",

        "really happy",

        "amazing day",

        "great day"

    ]


    if any(

        phrase in text

        for phrase in celebration_phrases

    ):

        return CELEBRATE


    # -----------------------------------------------------
    # CASUAL
    # -----------------------------------------------------

    casual_phrases = [

        "tell me a joke",

        "make me laugh",

        "i'm bored",
        "im bored",

        "let's talk",
        "lets talk",

        "say something"

    ]


    if any(

        phrase in text

        for phrase in casual_phrases

    ):

        return CASUAL


    # -----------------------------------------------------
    # COMFORT
    # -----------------------------------------------------

    emotional_phrases = [

        "sad",

        "hurt",

        "cry",
        "cried",
        "crying",

        "lonely",
        "alone",

        "exhausted",
        "drained",

        "overwhelmed",

        "scared",
        "afraid",

        "anxious",
        "anxiety",

        "angry",

        "upset",

        "disappointed",

        "grief",

        "lost",

        "empty",
        "numb",

        "bad day",

        "feel weird",
        "feel strange",

        "embarrassed",
        "embarrassing",

        "ashamed",

        "panic",
        "panicking",

        "worried"

    ]


    if any(

        phrase in text

        for phrase in emotional_phrases

    ):

        return COMFORT


    # -----------------------------------------------------
    # EXPLANATION / QUESTION
    # -----------------------------------------------------

    explanation_starters = [

        "what is ",
        "what are ",

        "why is ",
        "why are ",

        "how does ",
        "how do ",

        "can you explain",

        "what does ",

        "what happens",

        "is it normal"

    ]


    if (

        "?" in text

        or any(

            text.startswith(
                phrase
            )

            for phrase
            in explanation_starters

        )

    ):

        return EXPLAIN


    return GENERAL


# =========================================================
# SAFETY RESPONSE
# =========================================================

def generate_safety_response(
    message,
    continuing=False
):

    if continuing:

        return (
            "I want to stay with the safety part of this for "
            "a moment because of what you told me earlier. 💜\n\n"
            "Before we move on, I need to know whether you're "
            "safe right now. Are you in immediate danger of "
            "hurting yourself, or have you already done "
            "anything to hurt yourself?"
        )


    return (
        "I'm really glad you told me. 💜\n\n"
        "Please don't stay alone with this right now. Move "
        "somewhere with other people if you can, and put some "
        "distance between you and anything you could use to "
        "hurt yourself.\n\n"
        "If you think you might act on these thoughts or you've "
        "already hurt yourself, please get immediate emergency "
        "help or go to the nearest emergency department. You "
        "can also tell someone you trust directly: \"I'm having "
        "suicidal thoughts and I need you to stay with me.\"\n\n"
        "Are you in immediate danger of hurting yourself "
        "right now?"
    )