import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

# Load FAISS index
index = faiss.read_index(
    "vector_db/law_01_page_001.index"
)

# Load metadata
with open(
    "vector_db/law_01_page_001_metadata.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

# User query
query = "ច្បាប់ពាណិជ្ជកម្មតាមប្រព័ន្ធអេឡិចត្រូនិច"

# Convert query to embedding
query_embedding = model.encode([query])

query_embedding = np.array(query_embedding).astype("float32")

# Search top 3 chunks
distances, indices = index.search(query_embedding, k=3)

print("\nTop matching chunks:\n")

for i in indices[0]:

    chunk = chunks[i]

    print("=" * 50)
    print(f"Chunk ID: {chunk['chunk_id']}")
    print(chunk["text"])
    print()