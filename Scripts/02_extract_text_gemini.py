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

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

# Simple OCR prompt
prompt = """
Just read the image and write the text back exactly. Do not change anything.
"""

# Find all PNG pages
image_files = sorted(
    image_folder.glob("*.png")
)

# Counters
processed_pages = 0
skipped_pages = 0
failed_pages = 0

# Total runtime
start_time = time.time()

for image_path in image_files:

    # Example:
    # page_001.png
    page_name = image_path.stem

    # Extract page number
    page_number = int(
        page_name.split("_")[1]
    )

    # Output JSON path
    output_path = output_folder / (
        f"law_01_{page_name}.json"
    )

    # Skip existing pages
    if output_path.exists():

        print(
            f"Skipping already processed: "
            f"{page_name}"
        )

        skipped_pages += 1
        continue

    print(f"\nProcessing: {page_name}")

    # Per-page timer
    page_start_time = time.time()

    # Open image
    image = Image.open(image_path)

    # Retry settings
    max_retries = 10
    retry_count = 0

    success = False

    # Retry SAME PAGE until success
    while retry_count < max_retries:

        try:

            # Gemini OCR
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[prompt, image],
                config={
                    "temperature": 0
                }
            )

            extracted_text = response.text

            # Save JSON immediately
            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as f:

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

            success = True
            break

        except Exception as e:

            retry_count += 1

            # Exponential backoff
            wait_time = min(
                15 * retry_count,
                120
            )

            print(
                f"Error processing "
                f"{page_name}: {e}"
            )

            print(
                f"Retry "
                f"{retry_count}/{max_retries} "
                f"after waiting "
                f"{wait_time} seconds...\n"
            )

            time.sleep(wait_time)

    # If page failed after all retries
    if not success:

        print(
            f"Failed permanently: "
            f"{page_name}"
        )

        failed_pages += 1
        continue

    processed_pages += 1

    # Per-page runtime
    page_elapsed = (
        time.time() - page_start_time
    )

    print(
        f"Completed: {page_name} "
        f"({page_elapsed:.2f}s)"
    )

# Total runtime
elapsed_time = (
    time.time() - start_time
)

print("\n========== SUMMARY ==========")

print(
    f"Processed Pages : "
    f"{processed_pages}"
)

print(
    f"Skipped Pages   : "
    f"{skipped_pages}"
)

print(
    f"Failed Pages    : "
    f"{failed_pages}"
)

print(
    f"Total Runtime   : "
    f"{elapsed_time:.2f} seconds"
)

print(
    "OCR extraction completed successfully."
)