from tokenizer import cosine_similarity, embed_text
from client import client
import json


def retrieve_context(client, query, all_chunks, k=5):
    query_embedding = embed_text(client, query)

    scored = []
    for chunk in all_chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [x[1] for x in scored[:k]]


with open("embedded_docs.json", "r") as f:
    all_chunks = json.load(f)

docs_ordered_by_relevance = retrieve_context(
    client,
    "What was the total demand surcharge spend plus surge surcharge spend for tracking number 1Z97Y6036659856231",
    all_chunks,
)

for i, doc in enumerate(docs_ordered_by_relevance):
    print(f"Relevance score: {i+1}")
    print(doc["document_id"], doc["entity_name"], doc["chunk_text"])
