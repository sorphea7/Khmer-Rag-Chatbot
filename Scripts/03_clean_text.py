import json
import re
from pathlib import Path
import time

# Input folder
input_folder = Path(
    "data/extracted_text/raw/laws"
)

# Output folder
output_folder = Path(
    "data/extracted_text/cleaned/laws"
)

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

# Find all raw JSON files
json_files = sorted(
    input_folder.glob("*.json")
)

# Counters
processed_files = 0
skipped_files = 0

# Runtime
start_time = time.time()

for input_path in json_files:

    # Example:
    # law_01_page_001.json
    file_name = input_path.name

    # Output path
    output_path = output_folder / file_name

    # Skip existing cleaned file
    if output_path.exists():

        print(
            f"Skipping already cleaned: "
            f"{file_name}"
        )

        skipped_files += 1
        continue

    print(f"\nCleaning: {file_name}")

    # Load raw JSON
    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    raw_text = data["raw_text"]

    # -----------------------------
    # TEXT CLEANING
    # -----------------------------

    cleaned_text = raw_text

    # Normalize excessive line breaks
    cleaned_text = re.sub(
        r'\n{3,}',
        '\n\n',
        cleaned_text
    )

    # Remove excessive spaces/tabs
    cleaned_text = re.sub(
        r'[ \t]+',
        ' ',
        cleaned_text
    )

    # Remove trailing spaces
    cleaned_text = re.sub(
        r' +\n',
        '\n',
        cleaned_text
    )

    # Strip outer whitespace
    cleaned_text = cleaned_text.strip()

    # -----------------------------
    # SAVE CLEANED JSON
    # -----------------------------

    output_data = {
        "document_id": data["document_id"],
        "page": data["page"],
        "cleaned_text": cleaned_text
    }

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    processed_files += 1

    print(f"Completed: {file_name}")

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
    f"Total Runtime   : "
    f"{elapsed_time:.2f} seconds"
)

print(
    "Text cleaning completed successfully."
)