from dotenv import load_dotenv
import os

load_dotenv()  

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post_llm(persona, topic, context):

    prompt = f"""
You are a social media bot.

Personality:
{persona}

Topic:
{topic}

Context:
{context}

Write a strong opinionated post (max 280 characters).
Do not change your personality.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content