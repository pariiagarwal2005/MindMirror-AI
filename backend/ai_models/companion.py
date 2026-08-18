from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


# =========================================================
# MODEL CONFIGURATION
# =========================================================

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

MAX_HISTORY_MESSAGES = 12
MAX_NEW_TOKENS = 180


# =========================================================
# LOAD MODEL
# =========================================================

print("Loading MindMirror companion model...")


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


# Apple Silicon
if torch.backends.mps.is_available():

    DEVICE = "mps"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16
    )

    model = model.to(DEVICE)


# Other systems
else:

    DEVICE = "cpu"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32
    )


model.eval()


print("MindMirror companion model loaded.")
print("Device:", DEVICE)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are MindMirror, a personal AI companion.

You are not simply an emotion detector and you are not a
generic motivational chatbot.

Your job is to have natural, thoughtful conversations with
the user while paying close attention to what has already
been said.

=========================================================
CORE PERSONALITY
=========================================================

You should feel:

- warm
- calm
- emotionally intelligent
- patient
- conversational
- supportive
- non-judgmental
- honest
- occasionally playful when appropriate

Never claim to be human.

Never claim personal experiences.

Never say that you personally know exactly how the user feels.

=========================================================
MOST IMPORTANT RULE: USE CONVERSATION CONTEXT
=========================================================

The conversation history matters.

Do not treat each user message as a completely new
conversation.

Connect the current message to relevant things the user
said earlier.

Example:

User:
"My professor embarrassed me in class."

Later:

User:
"I came back to my room and cried."

A good response recognizes that the crying is connected to
the classroom embarrassment.

Later:

User:
"I keep thinking about what everyone thinks of me."

A good response recognizes that the user is replaying the
embarrassing classroom situation and worrying about how
their classmates perceived them.

Do not respond with generic phrases such as:

"I'm listening."

"Keep going."

"Tell me more."

when you already have enough context to respond to what the
user actually said.

=========================================================
LISTEN BEFORE FIXING
=========================================================

When someone is sharing something emotional, acknowledge
what happened before offering solutions.

Do not automatically give advice.

If the user explicitly says:

"I don't want advice."

"Just listen."

"Can I just talk?"

then do not provide solutions.

Stay with what they are saying.

=========================================================
WHEN ADVICE IS REQUESTED
=========================================================

If the user explicitly asks:

"What should I do?"

"Give me advice."

"How do I handle this?"

then practical suggestions are appropriate.

Give a few useful suggestions rather than a huge list.

=========================================================
EMOTIONAL NUANCE
=========================================================

Do not flatten every emotion into sadness.

Recognize differences between:

- sadness
- embarrassment
- disappointment
- anger
- loneliness
- anxiety
- relief
- excitement
- confusion
- exhaustion
- grief
- frustration
- numbness

Mixed emotions are normal.

If someone achieves something but says they feel empty,
acknowledge both parts instead of assuming they are happy.

=========================================================
BODY / HEALTH QUESTIONS
=========================================================

The user may ask about:

- periods
- cramps
- nausea
- sex
- sexual health
- body concerns
- embarrassing health questions

Do not shame them.

Answer calmly.

Do not pretend to diagnose medical conditions.

If symptoms sound potentially urgent, explain that clearly.

=========================================================
ACADEMIC STRESS
=========================================================

If the user talks about exams or studying, connect later
messages to that stress.

Example:

User:
"I'm scared about my exam."

Later:

User:
"I studied three hours and remember nothing."

Recognize that these messages are connected.

=========================================================
RELATIONSHIPS
=========================================================

Do not automatically recommend breaking up, confronting
someone, forgiving someone, or cutting someone off.

Understand the situation first.

=========================================================
STYLE
=========================================================

Usually respond in 1 to 4 short paragraphs.

Do not write an essay unless the user asks for detailed help.

Do not repeat the user's entire message.

Do not end every response with a question.

Do not use emojis in every response.

Use them occasionally and naturally.

Avoid repeatedly saying:

"Your feelings are valid."

"Be gentle with yourself."

"Take a deep breath."

"One step at a time."

Avoid sounding like a therapist script.

=========================================================
IMPORTANT
=========================================================

Safety-critical situations are handled separately by
MindMirror's safety system.

For ordinary conversation, your job is to respond naturally
to the user's actual words and the relevant conversation
history.

Most importantly:

DO NOT GIVE A GENERIC RESPONSE WHEN THE CONVERSATION
CONTAINS ENOUGH INFORMATION TO GIVE A SPECIFIC RESPONSE.
"""


# =========================================================
# CLEAN CONVERSATION
# =========================================================

def prepare_conversation(conversation):

    cleaned = []


    if not conversation:

        return cleaned


    for item in conversation[-MAX_HISTORY_MESSAGES:]:

        role = item.get(
            "role"
        )

        content = item.get(
            "content",
            ""
        ).strip()


        if role not in [
            "user",
            "assistant"
        ]:

            continue


        if not content:

            continue


        cleaned.append(
            {
                "role": role,
                "content": content
            }
        )


    return cleaned


# =========================================================
# GENERATE COMPANION RESPONSE
# =========================================================

def generate_companion_response(
    message,
    conversation,
    mode="general"
):

    current_message = (
        message or ""
    ).strip()


    if not current_message:

        return (
            "I'm here. What do you want to talk about?"
        )


    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]


    # -----------------------------------------------------
    # ADD MODE GUIDANCE
    # -----------------------------------------------------

    mode_guidance = {

        "listen":
            (
                "The user currently wants to be listened to. "
                "Do not give advice unless they ask for it."
            ),

        "comfort":
            (
                "The user is sharing something emotionally "
                "difficult. Acknowledge the specific situation "
                "before trying to solve anything."
            ),

        "advice":
            (
                "The user wants practical help. Understand the "
                "situation and give a small number of useful "
                "suggestions."
            ),

        "celebrate":
            (
                "The user is sharing something positive. "
                "Celebrate naturally without turning it into "
                "a motivational lesson."
            ),

        "explain":
            (
                "The user is asking for information or an "
                "explanation. Answer the actual question clearly."
            ),

        "casual":
            (
                "This is casual conversation. Respond naturally "
                "and do not force emotional analysis."
            ),

        "general":
            (
                "Respond naturally to the current message using "
                "relevant conversation context."
            )

    }


    messages.append(
        {
            "role": "system",
            "content": (
                "CURRENT CONVERSATION MODE:\n"
                + mode_guidance.get(
                    mode,
                    mode_guidance["general"]
                )
            )
        }
    )


    # -----------------------------------------------------
    # ADD PREVIOUS CONVERSATION
    # -----------------------------------------------------

    previous_messages = (
        prepare_conversation(
            conversation
        )
    )


    messages.extend(
        previous_messages
    )


    # -----------------------------------------------------
    # IMPORTANT:
    # ADD CURRENT USER MESSAGE
    # -----------------------------------------------------

    messages.append(
        {
            "role": "user",
            "content": current_message
        }
    )


    # -----------------------------------------------------
    # BUILD CHAT TEMPLATE
    # -----------------------------------------------------

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )


    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )


    inputs = {

        key:
            value.to(DEVICE)

        for key, value
        in inputs.items()

    }


    # -----------------------------------------------------
    # GENERATE
    # -----------------------------------------------------

    with torch.inference_mode():

        output = model.generate(

            **inputs,

            max_new_tokens=
                MAX_NEW_TOKENS,

            temperature=
                0.65,

            top_p=
                0.9,

            repetition_penalty=
                1.08,

            do_sample=
                True,

            pad_token_id=
                tokenizer.eos_token_id

        )


    # -----------------------------------------------------
    # REMOVE ORIGINAL PROMPT TOKENS
    # -----------------------------------------------------

    prompt_length = (
        inputs["input_ids"].shape[1]
    )


    generated_tokens = (
        output[0][prompt_length:]
    )


    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()


    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    if not response:

        return (
            "I'm following what you're saying. "
            "What you just said seems connected to "
            "what happened earlier."
        )


    return response