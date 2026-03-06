# RAG for P-Ticket Investigation

## Goal

The idea is that this RAG will be used internally by developers to help answer **P-tickets**.

Eventually, the RAG should be able to answer questions like:

> Tracking number `123` received **X discount** on charge_description `ABC`.  
> It should have instead received **Y discount**.  
> Why?

For now, even answering simpler questions would already be very useful.

The RAG can already generate **PySpark code** to answer questions such as:

- What is the total spend that the carrier billed on shipment `123`?
- What should the normalized surcharge be for `charge_description ABC` on tracking number `123`?

---

# How It Works

## 1. Context Documents

We maintain a **large repository of context documents** under:

These documents contain:

- Information about **Snowflake tables**
- Documentation for **specific PySpark helper functions** that we implement for the RAG

Example functions that may exist in the docs:

- `get_table`
- `get_shipment`
- `get_surcharge`
- `get_normalized_surcharge`

The purpose of these docs is to teach the model how to construct valid **PySpark transformations**.

---

## 2. Vectorization of Documents

All documents in `rag_docs` are **vectorized**.

Current implementation:

- Embeddings generated using **OpenAI**
- Stored locally in a **JSON file**

Eventually, once the number of documents grows large, we will need to store embeddings in a **cloud vector database**.

Example options in the future:

- Pinecone
- Weaviate
- pgvector
- Elasticsearch vector search

Note:

Experimenting with different **vectorizers** is an important part of data science.  
For now, OpenAI embeddings are sufficient.

---

## 3. Vectorize the User Query

When a user asks a question, the system:

1. Converts the **query into a vector embedding**
2. Uses the same embedding model used for the documents

---

## 4. Retrieve the Most Relevant Documents

The system compares the **query vector** with the **document vectors**.

Current similarity metric:

- **Cosine similarity**

Process:

1. Compute similarity between the query vector and every document vector
2. Retrieve the **top K most relevant documents**

These documents become the **context window** for the LLM.

Notes:

- Other similarity metrics could be used
- We may implement a **custom similarity metric** in the future

---

## 5. Generate PySpark Transformation

The RAG sends the **top K relevant documents** to the LLM.

Using these documents as context, the model constructs a **PySpark transformation** that answers the question.

---

# Example

## Question
What surcharge id should the surge surcharge for tracking number 1Z97Y6036659856231 get?

## Answer (Generated PySpark)

```python
(
    get_table("prod.charge.premodel")
    .where(
        (F.col("tracking_number") == "1Z97Y6036659856231")
        & (F.lower(F.col("charge_description")).like("%surge%"))
    )
    .transform(get_normalized_surcharge)
    .select("surcharge_id")
    .limit(1)
)
