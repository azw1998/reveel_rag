from client import client
from pathlib import Path
from retrieve_context import retrieve_context
import json


def get_simple_answer(client, question, schema_doc):
    return client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"""
    You generate Databricks SQL.
    Use the schema below.

    Schema:
    {schema_doc}

    Return SELECT-only SQL.
    """,
            },
            {"role": "user", "content": question},
        ],
    )


def main():
    file_path = Path("rag_docs/tables/premodel.txt")
    schema_doc = file_path.read_text(encoding="utf-8")

    question = "What surcharge id should the surge surcharge for tracking number 1Z97Y6036659856231 get?"
    # question = "What is the total spend for tracking number 1Z97Y6036659856231?"

    # answer = get_simple_answer(client, question, schema_doc)
    # print(answer.output_text)
    with open("embedded_docs.json", "r") as f:
        all_chunks = json.load(f)
    docs_ordered_by_relevance = retrieve_context(client, question, all_chunks, k=100)
    
    for i, doc in enumerate(docs_ordered_by_relevance):
        print(f"Relevance score: {i+1}")
        print(doc["document_id"], doc["entity_name"], doc["chunk_text"])


if __name__ == "__main__":
    main()
