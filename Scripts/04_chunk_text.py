import json
from pathlib import Path

# Input cleaned file
input_path = Path(
    "data/extracted_text/cleaned/laws/law_01_page_001.json"
)

# Output chunk file
output_path = Path(
    "data/chunked_documents/laws/law_01_page_001_chunks.json"
)

# Load cleaned JSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_text = data["cleaned_text"]

# Split by double newline
paragraphs = cleaned_text.split("\n\n")

chunks = []

for i, paragraph in enumerate(paragraphs):

    paragraph = paragraph.strip()

    if len(paragraph.split()) < 2:
      continue

    chunk = {
        "document_id": data["document_id"],
        "page": data["page"],
        "chunk_id": f"{data['document_id']}_page_{data['page']}_chunk_{i+1}",
        "text": paragraph
    }

    chunks.append(chunk)

# Create output directory
output_path.parent.mkdir(parents=True, exist_ok=True)

# Save chunks
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"Created {len(chunks)} chunks.")