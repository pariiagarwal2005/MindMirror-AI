def generate_reflection(text, emotion):

    reflections = {

        "sadness": 
        "You seem to be going through a difficult emotional phase. "
        "Try giving yourself some time, take small steps, and talk to someone you trust.",


        "fear":
        "It looks like you may be feeling overwhelmed or uncertain. "
        "Try breaking your challenges into smaller tasks and focus on one step at a time.",


        "anger":
        "It seems like something is bothering you deeply. "
        "Taking a pause and reflecting before reacting may help you process these feelings.",


        "joy":
        "It is wonderful to see positive emotions. "
        "Try remembering these moments and what contributed to your happiness.",


        "surprise":
        "Something unexpected seems to have affected you. "
        "Take some time to understand how this experience made you feel.",


        "neutral":
        "Your thoughts seem balanced today. "
        "Continue reflecting on your emotions and experiences."
    }


    return reflections.get(
        emotion,
        "Keep reflecting on your thoughts and emotions. "
        "Understanding yourself is an important step."
    )