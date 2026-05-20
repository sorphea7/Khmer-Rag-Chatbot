import json
import time
import faiss
import numpy as np
import streamlit as st
from google import genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Khmer Legal Chatbot",
    layout="wide"
)

# -----------------------------
# LOAD ENV
# -----------------------------

load_dotenv()

# -----------------------------
# GEMINI CLIENT
# -----------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# CACHED RESOURCES
# -----------------------------

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

@st.cache_resource
def load_faiss_index():

    return faiss.read_index(
        "vector_db/law_01.index"
    )

@st.cache_resource
def load_metadata():

    with open(
        "vector_db/law_01_metadata.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

# Load resources
embedding_model = load_embedding_model()

index = load_faiss_index()

chunks = load_metadata()

# -----------------------------
# UI
# -----------------------------

st.title("Khmer Legal Chatbot")

st.write(
    "RAG chatbot test using Khmer legal documents."
)

query = st.text_area(
    "Ask a question in Khmer:"
)

# -----------------------------
# ASK BUTTON
# -----------------------------

if st.button("Ask") and query.strip():

    with st.spinner("Searching documents..."):

        # -----------------------------
        # EMBED QUERY
        # -----------------------------

        query_embedding = embedding_model.encode(
            [query]
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        # -----------------------------
        # VECTOR SEARCH
        # -----------------------------

        distances, indices = index.search(
            query_embedding,
            k=5
        )

        # -----------------------------
        # BUILD CONTEXT
        # -----------------------------

        retrieved_chunks = []

        for rank, i in enumerate(indices[0]):

            chunk = chunks[i]

            retrieved_chunks.append(
                f"""
[Source {rank + 1}]
Document ID: {chunk["document_id"]}
Page: {chunk["page"]}
Chunk ID: {chunk["chunk_id"]}

{chunk["text"]}
"""
            )

        context = "\n\n".join(
            retrieved_chunks
        )

        # -----------------------------
        # RAG PROMPT
        # -----------------------------

        prompt = f"""
You are a Khmer legal document assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do NOT use outside knowledge.
- Do NOT invent information.
- Do NOT hallucinate laws.
- If the answer is not found in the context, say:
  "រកមិនឃើញព័ត៌មាននេះនៅក្នុងឯកសារដែលបានផ្តល់។"
- Answer in Khmer.
- Mention page numbers if relevant.

Context:
{context}

Question:
{query}
"""

        # -----------------------------
        # GEMINI RETRY LOGIC
        # -----------------------------

        max_retries = 5
        retry_count = 0

        response = None

        while retry_count < max_retries:

            try:

                response = client.models.generate_content(
                    ## change to different model using for answering question which is cheaper.
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "temperature": 0
                    }
                )

                break

            except Exception as e:

                retry_count += 1

                wait_time = retry_count * 10

                st.warning(
                    f"Gemini busy. "
                    f"Retry {retry_count}/{max_retries} "
                    f"after {wait_time}s..."
                )

                time.sleep(wait_time)

        # -----------------------------
        # FAILURE
        # -----------------------------

        if response is None:

            st.error(
                "Gemini is currently overloaded. "
                "Please try again later."
            )

            st.stop()

    # -----------------------------
    # ANSWER
    # -----------------------------

    st.subheader("Answer")

    st.write(response.text)

    # -----------------------------
    # SOURCES
    # -----------------------------

    st.subheader(
        "Retrieved Sources"
    )

    for rank, i in enumerate(indices[0]):

        chunk = chunks[i]

        with st.expander(
            f"Rank {rank + 1} | "
            f"Page {chunk['page']} | "
            f"Distance "
            f"{distances[0][rank]:.4f}"
        ):

            st.write(chunk["text"])