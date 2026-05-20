import json
from pathlib import Path
import time

# Root cleaned folder
input_root = Path(
    "data/extracted_text/cleaned"
)

# Root chunk output folder
output_root = Path(
    "data/chunked_documents"
)

output_root.mkdir(
    parents=True,
    exist_ok=True
)

# Find ALL cleaned JSON files
json_files = sorted(
    input_root.rglob("*.json")
)

# Counters
processed_files = 0
skipped_files = 0
total_chunks = 0

# Runtime
start_time = time.time()

for input_path in json_files:

    # Example:
    # laws/law_01_page_001.json
    relative_path = input_path.relative_to(
        input_root
    )

    # Convert filename
    output_filename = (
        input_path.stem + "_chunks.json"
    )

    # Preserve folder structure
    output_path = (
        output_root
        / relative_path.parent
        / output_filename
    )

    # Create folders
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Skip existing chunks
    if output_path.exists():

        print(
            f"Skipping already chunked: "
            f"{relative_path}"
        )

        skipped_files += 1
        continue

    print(f"\nChunking: {relative_path}")

    # Load cleaned JSON
    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    cleaned_text = data["cleaned_text"]

    # Split by double newline
    paragraphs = cleaned_text.split("\n\n")

    chunks = []

    for i, paragraph in enumerate(paragraphs):

        paragraph = paragraph.strip()

        # Safe Khmer filtering
        if len(paragraph) == 0:
            continue

        chunk = {
            "document_id": data["document_id"],
            "page": data["page"],
            "chunk_id": (
                f"{data['document_id']}"
                f"_page_{data['page']}"
                f"_chunk_{i+1}"
            ),
            "text": paragraph
        }

        chunks.append(chunk)

    # Save chunk file
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    processed_files += 1
    total_chunks += len(chunks)

    print(
        f"Created {len(chunks)} chunks."
    )

# Total runtime
elapsed_time = (
    time.time() - start_time
)

print("\n========== SUMMARY ==========")

print(
    f"Processed Files : "
    f"{processed_files}"
)

print(
    f"Skipped Files   : "
    f"{skipped_files}"
)

print(
    f"Total Chunks    : "
    f"{total_chunks}"
)

print(
    f"Total Runtime   : "
    f"{elapsed_time:.2f} seconds"
)

print(
    "Chunking completed successfully."
)