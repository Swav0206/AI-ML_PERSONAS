from sentence_transformers import SentenceTransformer
import numpy as np
from data.personas import bots

model = SentenceTransformer('all-MiniLM-L6-v2')

bot_vectors = {k: model.encode(v) for k, v in bots.items()}

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def route_post(post, threshold=0.4):
    post_vec = model.encode(post)
    matched = []

    for bot, vec in bot_vectors.items():
        score = cosine_similarity(post_vec, vec)
        if score > threshold:
            matched.append((bot, round(score, 2)))

    return matched