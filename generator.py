from llm import generate_post_llm

def generate_post(bot_id, persona, user_input):

    topic = user_input
    context = f"Recent discussion about {topic}"

    post = generate_post_llm(persona, topic, context)

    return {
        "bot_id": bot_id,
        "topic": topic,
        "post_content": post[:280]
    }