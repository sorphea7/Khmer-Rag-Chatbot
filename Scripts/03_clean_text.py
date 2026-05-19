import json
import re
from pathlib import Path

# Input file
input_path = Path(
    "data/extracted_text/raw/laws/law_01_page_001.json"
)

# Output file
output_path = Path(
    "data/extracted_text/cleaned/laws/law_01_page_001.json"
)

# Load raw JSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

raw_text = data["raw_text"]

# Cleaning
cleaned_text = raw_text

# Normalize line breaks
cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

# Remove excessive spaces
cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)

# Remove leading/trailing whitespace
cleaned_text = cleaned_text.strip()

# Save cleaned JSON
output_data = {
    "document_id": data["document_id"],
    "page": data["page"],
    "cleaned_text": cleaned_text
}

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(
        output_data,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Text cleaned successfully.")