from google import genai
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Input folder (ONE PDF ONLY)
image_folder = Path(
    "data/page_images/laws/law_01"
)

# Output folder
output_folder = Path(
    "data/extracted_text/raw/laws"
)

output_folder.mkdir(parents=True, exist_ok=True)

# Prompt
prompt = """
Extract ALL text from this document page.

Rules:
- Preserve original Khmer and English text
- Do NOT summarize
- Do NOT translate
- Preserve paragraph structure
- Output only extracted text
"""

# Find all PNG pages
image_files = sorted(image_folder.glob("*.png"))

# Counters
processed_pages = 0
skipped_pages = 0

for image_path in image_files:

    # Example:
    # page_001.png
    page_name = image_path.stem

    # Extract page number
    page_number = int(page_name.split("_")[1])

    # Output JSON path
    output_path = output_folder / f"law_01_{page_name}.json"

    # Skip if already processed
    if output_path.exists():

        print(f"Skipping already processed: {page_name}")

        skipped_pages += 1
        continue

    print(f"\nProcessing: {page_name}")

    # Open image
    image = Image.open(image_path)

    # Gemini OCR
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    extracted_text = response.text

    # Save JSON immediately
    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            {
                "document_id": "law_01",
                "page": page_number,
                "raw_text": extracted_text
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    processed_pages += 1

    print(f"Completed: {page_name}")

    # Rate limit safety
    time.sleep(5)

print("\n========== SUMMARY ==========")
print(f"Processed Pages : {processed_pages}")
print(f"Skipped Pages   : {skipped_pages}")
print("OCR extraction completed successfully.")