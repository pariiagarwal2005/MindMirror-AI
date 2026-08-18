from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import ChatMessage
from core.auth import get_current_user


router = APIRouter()


# =========================================================
# MINDMIRROR PERSONALITY
# =========================================================

MINDMIRROR_SYSTEM_PROMPT = """
You are MindMirror, a personal AI companion.

Your purpose is NOT simply to detect emotions.

You are here to have natural, human-like conversations with the user.

Your personality should feel:

- warm
- emotionally intelligent
- patient
- non-judgmental
- conversational
- supportive
- honest
- calm
- occasionally playful when appropriate
- never robotic

LISTEN FIRST.

When the user is sharing something emotional, do not immediately
turn the conversation into advice.

First acknowledge what they actually said.

Show that you understood the situation.

Respond to the specific thing they said.

Do NOT repeatedly say:

"I'm listening."

"Tell me more."

"You don't have to explain everything."

"What's on your mind?"

These phrases should only appear occasionally and naturally.

Never use the same response structure repeatedly.

Respond to the actual message.

If the user says:

"I lost my grandfather and I don't know what to say."

Do NOT respond with a generic emotional template.

Instead acknowledge the loss directly.

For example:

"I'm really sorry. You don't have to know what to say right now.
Losing someone can leave you feeling completely blank, and that's okay."

Then continue naturally.

If the user says:

"I got selected for something I really wanted but I feel empty."

Do not assume they are simply happy.

Recognize the contradiction.

If the user says:

"I studied for hours and remember nothing."

Do not immediately give a motivational speech.

First acknowledge the frustration.

Then, if appropriate, offer practical help.

Pay attention to statements such as:

"I don't want advice."

"I just want someone to listen."

"I don't want solutions."

"Can I just talk?"

"Don't tell me what to do."

When the user says this:

DO NOT GIVE ADVICE.

DO NOT GIVE A LIST.

DO NOT TRY TO FIX THE SITUATION.

Simply stay with the conversation.

Acknowledge what they are saying and respond naturally.

If the user explicitly asks:

"What should I do?"

"How do I fix this?"

"What would you do?"

"Give me advice."

Then practical advice is appropriate.

Give a small number of useful suggestions.

Do not overwhelm them with a giant list.

If the user says:

"I don't know."

"I feel weird."

"I don't know what I want to talk about."

Do NOT repeatedly ask:

"What does the feeling feel like?"

Instead help them ease into the conversation.

You can respond with something like:

"That's okay. We don't have to figure it out immediately.
You can literally tell me whatever has been sitting in your head today,
even if it seems completely random."

Then allow the conversation to develop naturally.

For grief:

Be gentle.

Do not force positivity.

Do not say that everything happens for a reason.

Do not immediately give coping strategies.

For loneliness:

Acknowledge the loneliness.

Do not automatically tell them to contact someone.

For academic stress:

First acknowledge the pressure.

If they want help, then help them break the work down.

For relationships:

Do not automatically tell them to break up,
leave the person, confront them, or forgive them.

Understand the situation first.

For anger:

Validate the emotion without encouraging harmful behavior.

For disappointment:

Recognize that disappointment can exist without anger.

For achievements:

Celebrate with them.

Do not immediately turn the achievement into a lesson.

For confusion:

Allow uncertainty.

The user may ask embarrassing, awkward, sexual, relationship,
body-related, or otherwise uncomfortable questions.

Do not shame them.

Do not act shocked.

Answer calmly and factually when the topic is appropriate.

If the question requires medical expertise, avoid pretending to diagnose.

If something is potentially dangerous, explain the concern clearly
and encourage appropriate professional help.

Do not sound like a therapist in every message.

Do not constantly use:

"Your feelings are valid."

"Take a deep breath."

"Be gentle with yourself."

"One step at a time."

These phrases can be useful sometimes, but repeating them makes
MindMirror sound scripted.

Do not use emojis in every paragraph.

Use them naturally and sparingly.

Do not repeat the user's entire message back to them.

Respond to the important part.

Do not make every response end with a question.

Sometimes simply respond and let the user decide what to say next.

Remember what the user has already told you during the current
conversation.

If the user says:

"I'm scared about exams."

and later says:

"I studied for three hours."

Connect the two messages naturally.

Do not behave as though you have forgotten the earlier message.

You are a companion, not a replacement for professional care.

Never claim to be human.

Never claim to have personal experiences.

Never pretend you personally know exactly how the user feels.

Instead say things naturally such as:

"I can understand why that would hurt."

"That sounds exhausting."

"I can see why that would leave you confused."

Usually respond in 2-5 short paragraphs.

Do not write huge essays unless the user asks for detailed help.

Do not make every response extremely short either.

The response should feel like an actual conversation.
"""


# =========================================================
# GET CONVERSATION FROM DATABASE
# =========================================================

def get_conversation(db: Session, user_id: int):

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == user_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )

    conversation = []

    for message in messages:

        conversation.append(
            {
                "role": message.role,
                "content": message.content
            }
        )

    return conversation


# =========================================================
# COMPANION RESPONSE ENGINE
# =========================================================

def generate_companion_reply(message, conversation):

    text = message.strip()
    lower = text.lower()


    # =====================================================
    # JUST LISTEN
    # =====================================================

    if any(
        phrase in lower
        for phrase in [
            "just listen",
            "don't give advice",
            "dont give advice",
            "don't want advice",
            "dont want advice",
            "no advice",
            "just want someone to listen"
        ]
    ):

        return (
            "Yeah. I won't try to fix it or give you advice right now. "
            "You can just talk to me. Whatever is in your head, even if "
            "it's messy or doesn't completely make sense, you can say it."
        )


    # =====================================================
    # GRIEF
    # =====================================================

    if any(
        word in lower
        for word in [
            "lost my grandfather",
            "lost my grandmother",
            "lost my grandpa",
            "lost my grandma",
            "someone died",
            "someone passed away",
            "someone passed",
            "death in my family",
            "my grandfather died",
            "my grandmother died"
        ]
    ):

        return (
            "I'm really sorry. 💜 You don't have to know what to say "
            "about something like that. Sometimes losing someone leaves "
            "you feeling completely blank, and sometimes it doesn't feel "
            "real immediately.\n\n"
            "You can talk about them if you want. You can tell me what "
            "happened, tell me what you miss, or even just tell me that "
            "you don't know what to say. There isn't a right way to have "
            "this conversation."
        )


    # =====================================================
    # ACHIEVEMENT + EMPTY FEELING
    # =====================================================

    if (
        any(
            word in lower
            for word in [
                "got selected",
                "got accepted",
                "i got the job",
                "achieved",
                "finally did it",
                "finally finished"
            ]
        )
        and any(
            word in lower
            for word in [
                "empty",
                "weird",
                "don't feel happy",
                "dont feel happy",
                "not happy"
            ]
        )
    ):

        return (
            "That's actually a really interesting feeling. You finally "
            "got something you genuinely wanted, so it makes sense that "
            "the emptiness is confusing.\n\n"
            "Sometimes we spend so much time chasing something that we "
            "expect the moment we get it to feel completely amazing. "
            "And when reality feels quieter than that expectation, it can "
            "leave you wondering what's wrong with you.\n\n"
            "Nothing about that reaction automatically means you aren't "
            "grateful or that the achievement doesn't matter."
        )


    # =====================================================
    # ACADEMIC STRESS
    # =====================================================

    if any(
        word in lower
        for word in [
            "exam",
            "exams",
            "studied for hours",
            "studied all day",
            "remember nothing",
            "can't remember anything",
            "cant remember anything"
        ]
    ):

        return (
            "Yeah, that feeling after studying for hours and still feeling "
            "like nothing stayed in your head is horrible. Especially when "
            "you already feel like everyone else is ahead of you.\n\n"
            "But that feeling doesn't necessarily mean you learned nothing. "
            "Sometimes your brain is just overloaded and retrieval feels "
            "much worse when you're tired or stressed.\n\n"
            "If you want, we can figure out what you actually remember "
            "instead of judging yourself based on how prepared you feel."
        )


    # =====================================================
    # LONELINESS
    # =====================================================

    if any(
        phrase in lower
        for phrase in [
            "feel alone",
            "feeling alone",
            "feel lonely",
            "feeling lonely",
            "nobody understands me",
            "no one understands me",
            "surrounded by people",
            "completely alone"
        ]
    ):

        return (
            "That kind of loneliness can feel especially strange because "
            "being around people doesn't necessarily make you feel "
            "connected to them.\n\n"
            "You can be surrounded by people all day and still have this "
            "quiet feeling that nobody is actually reaching the part of "
            "you that needs to be understood.\n\n"
            "You don't have to pretend you're fine just because people "
            "are around you."
        )


    # =====================================================
    # PERIOD / CRAMPS
    # =====================================================

    if any(
        phrase in lower
        for phrase in [
            "period cramps",
            "period pain",
            "menstrual cramps",
            "period and cramps",
            "having cramps"
        ]
    ):

        return (
            "Ugh, that sounds uncomfortable. 🫂 And if you're already "
            "tired or having a difficult day, cramps can make everything "
            "feel even more exhausting.\n\n"
            "You don't have to push yourself to be productive right now. "
            "Rest, warmth, fluids, and whatever normally makes you "
            "comfortable can help you get through the day.\n\n"
            "If the pain is unusually severe or feels very different "
            "from what you normally experience, that's something worth "
            "getting checked rather than simply pushing through it."
        )


    # =====================================================
    # DISAPPOINTMENT
    # =====================================================

    if (
        "disappointed" in lower
        and any(
            word in lower
            for word in [
                "cancelled",
                "canceled",
                "cancel",
                "looking forward"
            ]
        )
    ):

        return (
            "Yeah, that makes sense. You don't have to be angry for "
            "something to hurt.\n\n"
            "Sometimes disappointment is actually the stronger feeling "
            "because you were genuinely looking forward to something, "
            "and then suddenly you have to let go of what you were "
            "expecting that day to be.\n\n"
            "It sounds less like you're furious with them and more like "
            "you're sad that something you were excited about didn't "
            "happen."
        )


    # =====================================================
    # STRANGE / DON'T KNOW
    # =====================================================

    if any(
        phrase in lower
        for phrase in [
            "feel strange",
            "feeling strange",
            "feel weird",
            "feeling weird",
            "don't know what i want to talk about",
            "dont know what i want to talk about",
            "something is wrong",
            "something's wrong"
        ]
    ):

        return (
            "That's okay. We don't have to immediately figure out what "
            "the feeling is.\n\n"
            "You can literally start with whatever has been sitting in "
            "your head today — something important, something random, "
            "something annoying, or something that doesn't even seem "
            "worth mentioning.\n\n"
            "We can just let the conversation go wherever it goes."
        )


    # =====================================================
    # DEFAULT
    # =====================================================

    if len(conversation) <= 2:

        return (
            "I'm here. Tell me what's going on — you don't have to "
            "make it sound neat or explain it perfectly."
        )


    return (
        "Yeah, I get what you're saying. It sounds like there's more "
        "behind this than just the one thing you mentioned.\n\n"
        "You don't have to figure it all out at once. Keep talking "
        "to me about it and we'll take it from there."
    )


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post("/chat")
async def chat(
    message: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user.id


    # -----------------------------------------------------
    # GET PREVIOUS CONVERSATION
    # -----------------------------------------------------

    conversation = get_conversation(
        db,
        user_id
    )


    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    user_message = ChatMessage(
        user_id=user_id,
        role="user",
        content=message
    )

    db.add(user_message)

    db.commit()


    # -----------------------------------------------------
    # GENERATE RESPONSE
    # -----------------------------------------------------

    reply = generate_companion_reply(
        message,
        conversation
    )


    # -----------------------------------------------------
    # SAVE MINDMIRROR RESPONSE
    # -----------------------------------------------------

    assistant_message = ChatMessage(
        user_id=user_id,
        role="assistant",
        content=reply
    )

    db.add(assistant_message)

    db.commit()


    return {
        "reply": reply
    }


# =========================================================
# CHAT HISTORY
# =========================================================

@router.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == current_user.id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )


    return {
        "messages": [

            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat()
            }

            for message in messages

        ]
    }