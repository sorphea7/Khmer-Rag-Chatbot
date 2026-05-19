import google.generativeai as genai
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Input image
image_path = "data/page_images/laws/law_01/page_001.png"

# Open image
image = Image.open(image_path)

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

# Generate response
response = model.generate_content([prompt, image])

# Extract text
extracted_text = response.text

# Output path
output_path = Path(
    "data/extracted_text/raw/laws/law_01_page_001.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

# Save JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(
        {
            "document_id": "law_01",
            "page": 1,
            "raw_text": extracted_text
        },
        f,
        ensure_ascii=False,
        indent=2
    )

print("Text extraction completed.")