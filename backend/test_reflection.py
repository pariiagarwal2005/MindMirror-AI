from ai_models.reflection_generator import generate_reflection


text = "I am on my periods, i feel tired and sad"

emotion = "sadness"


result = generate_reflection(
    text,
    emotion
)


print(result)
