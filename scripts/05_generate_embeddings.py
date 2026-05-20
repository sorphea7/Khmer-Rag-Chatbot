import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import time

# Load embedding model
model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

# Root chunk folder
input_root = Path(
    "data/chunked_documents/laws"
)

# Output vector DB folder
output_root = Path(
    "vector_db"
)

output_root.mkdir(
    parents=True,
    exist_ok=True
)

# Find ALL chunk JSON files
chunk_files = sorted(
    input_root.glob("*_chunks.json")
)

# Store all chunks
all_chunks = []

# Runtime
start_time = time.time()

print("Loading chunk files...")

# Load all chunk files
for chunk_path in chunk_files:

    print(f"Loading: {chunk_path.name}")

    with open(
        chunk_path,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

        all_chunks.extend(chunks)

print(
    f"\nTotal chunks loaded: "
    f"{len(all_chunks)}"
)

# Extract text only
texts = [
    chunk["text"]
    for chunk in all_chunks
]

print("\nGenerating embeddings...")

# Generate embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True
)

# Convert to numpy float32
embeddings = np.array(
    embeddings
).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(embeddings)

print(
    f"\nFAISS index size: "
    f"{index.ntotal}"
)

# -----------------------------
# SAVE VECTOR DATABASE
# -----------------------------

# Save FAISS index
faiss_output = (
    output_root / "law_01.index"
)

faiss.write_index(
    index,
    str(faiss_output)
)

# Save metadata
metadata_output = (
    output_root / "law_01_metadata.json"
)

with open(
    metadata_output,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

# Total runtime
elapsed_time = (
    time.time() - start_time
)

print("\n========== SUMMARY ==========")

print(
    f"Chunk Files Loaded : "
    f"{len(chunk_files)}"
)

print(
    f"Total Chunks       : "
    f"{len(all_chunks)}"
)

print(
    f"Embedding Dimension: "
    f"{dimension}"
)

print(
    f"Vector Count       : "
    f"{index.ntotal}"
)

print(
    f"Total Runtime      : "
    f"{elapsed_time:.2f} seconds"
)

print(
    "\nEmbeddings and FAISS "
    "index created successfully."
)