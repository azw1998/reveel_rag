from tokenizer import cosine_similarity, embed_text
from client import client
import json


def retrieve_context(client, query, all_chunks, k=5):
    query_embedding = embed_text(client, query)

    scored = []
    for chunk in all_chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored.append({"score": score, "chunk": chunk})

    scored.sort(key=lambda x: x["score"], reverse=True)

    return [x["chunk"] for x in scored[:k]]
