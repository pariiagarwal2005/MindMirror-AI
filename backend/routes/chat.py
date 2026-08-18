from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.database import get_db
from database.models import ChatMessage

from core.auth import get_current_user

from ai_models.companion_engine import (
    detect_mode,
    contains_safety_signal,
    says_safe_now,
    SAFETY,
    generate_safety_response
)

from ai_models.companion import (
    generate_companion_response
)

import uuid


router = APIRouter()


# =========================================================
# CREATE CONVERSATION ID
# =========================================================

def create_conversation_id():

    return str(
        uuid.uuid4()
    )


# =========================================================
# GENERATE TITLE
# =========================================================

def generate_title(message):

    text = (
        message or ""
    ).strip()


    if not text:

        return "New conversation"


    text = " ".join(
        text.split()
    )


    if len(text) > 45:

        return (
            text[:45].rstrip()
            + "..."
        )


    return text


# =========================================================
# CONVERSATION SAFETY STATE
# =========================================================

def conversation_has_active_safety_state(
    conversation
):

    """
    Search backwards through user messages.

    A safety statement activates safety mode.

    A later explicit statement that the user is safe
    clears that state.
    """


    for item in reversed(
        conversation
    ):

        if (
            item.get("role")
            != "user"
        ):

            continue


        content = item.get(
            "content",
            ""
        )


        if says_safe_now(
            content
        ):

            return False


        if contains_safety_signal(
            content
        ):

            return True


    return False


# =========================================================
# GET ALL CONVERSATIONS
# =========================================================

@router.get("/conversations")
async def get_conversations(

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_user
    )

):

    user_id = (
        current_user.id
    )


    conversation_rows = (

        db.query(

            ChatMessage.conversation_id,

            func.max(
                ChatMessage.created_at
            ).label(
                "updated_at"
            )

        )

        .filter(

            ChatMessage.user_id
            == user_id,

            ChatMessage.conversation_id
            .isnot(None)

        )

        .group_by(
            ChatMessage.conversation_id
        )

        .order_by(
            func.max(
                ChatMessage.created_at
            ).desc()
        )

        .all()

    )


    conversations = []


    for row in conversation_rows:

        conversation_id = (
            row.conversation_id
        )


        messages = (

            db.query(
                ChatMessage
            )

            .filter(

                ChatMessage.user_id
                == user_id,

                ChatMessage.conversation_id
                == conversation_id

            )

            .order_by(
                ChatMessage.created_at.asc()
            )

            .all()

        )


        if not messages:

            continue


        first_user_message = next(

            (

                item

                for item
                in messages

                if item.role
                == "user"

            ),

            None

        )


        title = (

            generate_title(
                first_user_message.content
            )

            if first_user_message

            else "New conversation"

        )


        conversations.append(

            {

                "conversation_id":
                    conversation_id,

                "title":
                    title,

                "created_at":
                    (
                        messages[0]
                        .created_at
                        .isoformat()

                        if messages[0]
                        .created_at

                        else None
                    ),

                "updated_at":
                    (
                        messages[-1]
                        .created_at
                        .isoformat()

                        if messages[-1]
                        .created_at

                        else None
                    ),

                "message_count":
                    len(messages)

            }

        )


    return {

        "conversations":
            conversations

    }


# =========================================================
# GET ONE CONVERSATION
# =========================================================

@router.get(
    "/conversations/{conversation_id}"
)
async def get_conversation(

    conversation_id: str,

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_user
    )

):

    user_id = (
        current_user.id
    )


    messages = (

        db.query(
            ChatMessage
        )

        .filter(

            ChatMessage.user_id
            == user_id,

            ChatMessage.conversation_id
            == conversation_id

        )

        .order_by(
            ChatMessage.created_at.asc()
        )

        .all()

    )


    if not messages:

        raise HTTPException(

            status_code=404,

            detail=(
                "Conversation not found"
            )

        )


    first_user_message = next(

        (

            item

            for item
            in messages

            if item.role
            == "user"

        ),

        None

    )


    title = (

        generate_title(
            first_user_message.content
        )

        if first_user_message

        else "New conversation"

    )


    return {

        "conversation_id":
            conversation_id,

        "title":
            title,

        "messages":

            [

                {

                    "id":
                        item.id,

                    "role":
                        item.role,

                    "content":
                        item.content,

                    "created_at":
                        (
                            item.created_at
                            .isoformat()

                            if item.created_at

                            else None
                        )

                }

                for item
                in messages

            ]

    }


# =========================================================
# CHAT
# =========================================================

@router.post("/")
async def chat(

    message: str,

    conversation_id: str = None,

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_user
    )

):

    user_id = (
        current_user.id
    )


    current_message = (
        message or ""
    ).strip()


    if not current_message:

        raise HTTPException(

            status_code=400,

            detail=(
                "Message cannot be empty."
            )

        )


    # =====================================================
    # CREATE / VALIDATE CONVERSATION
    # =====================================================

    if not conversation_id:

        conversation_id = (
            create_conversation_id()
        )


    else:

        existing = (

            db.query(
                ChatMessage
            )

            .filter(

                ChatMessage.user_id
                == user_id,

                ChatMessage.conversation_id
                == conversation_id

            )

            .first()

        )


        if not existing:

            raise HTTPException(

                status_code=404,

                detail=(
                    "Conversation not found"
                )

            )


    # =====================================================
    # LOAD PREVIOUS CONVERSATION
    # =====================================================

    previous_messages = (

        db.query(
            ChatMessage
        )

        .filter(

            ChatMessage.user_id
            == user_id,

            ChatMessage.conversation_id
            == conversation_id

        )

        .order_by(
            ChatMessage.created_at.asc()
        )

        .all()

    )


    conversation_data = [

        {

            "role":
                item.role,

            "content":
                item.content

        }

        for item
        in previous_messages

    ]


    # =====================================================
    # SAFETY STATE BEFORE CURRENT MESSAGE
    # =====================================================

    safety_was_active = (
        conversation_has_active_safety_state(
            conversation_data
        )
    )


    current_is_safety = (
        contains_safety_signal(
            current_message
        )
    )


    current_says_safe = (
        says_safe_now(
            current_message
        )
    )


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    user_message = ChatMessage(

        user_id=
            user_id,

        conversation_id=
            conversation_id,

        role=
            "user",

        content=
            current_message

    )


    db.add(
        user_message
    )

    db.commit()

    db.refresh(
        user_message
    )


    # =====================================================
    # GENERATE RESPONSE
    # =====================================================

    if current_is_safety:

        reply = (
            generate_safety_response(
                current_message,
                continuing=False
            )
        )


    elif (
        safety_was_active
        and not current_says_safe
    ):

        reply = (
            generate_safety_response(
                current_message,
                continuing=True
            )
        )


    else:

        mode = (
            detect_mode(
                current_message
            )
        )


        # SAFETY should already have been
        # handled above.

        if mode == SAFETY:

            reply = (
                generate_safety_response(
                    current_message,
                    continuing=False
                )
            )


        else:

            reply = (
                generate_companion_response(

                    current_message,

                    conversation_data,

                    mode=mode

                )
            )


    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    assistant_message = ChatMessage(

        user_id=
            user_id,

        conversation_id=
            conversation_id,

        role=
            "assistant",

        content=
            reply

    )


    db.add(
        assistant_message
    )

    db.commit()

    db.refresh(
        assistant_message
    )


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "reply":
            reply,

        "conversation_id":
            conversation_id,

        "message_id":
            assistant_message.id,

        "mode":
            (
                SAFETY

                if (
                    current_is_safety
                    or (
                        safety_was_active
                        and not current_says_safe
                    )
                )

                else detect_mode(
                    current_message
                )
            )

    }


# =========================================================
# DELETE CONVERSATION
# =========================================================

@router.delete(
    "/conversations/{conversation_id}"
)
async def delete_conversation(

    conversation_id: str,

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_user
    )

):

    user_id = (
        current_user.id
    )


    messages = (

        db.query(
            ChatMessage
        )

        .filter(

            ChatMessage.user_id
            == user_id,

            ChatMessage.conversation_id
            == conversation_id

        )

        .all()

    )


    if not messages:

        raise HTTPException(

            status_code=404,

            detail=(
                "Conversation not found"
            )

        )


    for item in messages:

        db.delete(
            item
        )


    db.commit()


    return {

        "message":
            "Conversation deleted successfully",

        "conversation_id":
            conversation_id

    }