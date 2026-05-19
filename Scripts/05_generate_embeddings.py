import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

# Input chunk file
input_path = Path(
    "data/chunked_documents/laws/law_01_page_001_chunks.json"
)

# Load chunks
with open(input_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]

# Generate embeddings
embeddings = model.encode(texts)

# Convert to numpy float32
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(embeddings)

# Save FAISS index
faiss_output = "vector_db/law_01_page_001.index"

Path("vector_db").mkdir(parents=True, exist_ok=True)

faiss.write_index(index, faiss_output)

# Save metadata
metadata_output = "vector_db/law_01_page_001_metadata.json"

with open(metadata_output, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("Embeddings and FAISS index created successfully.")