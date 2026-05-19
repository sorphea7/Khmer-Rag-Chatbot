from pdf2image import convert_from_path
from pathlib import Path

# Root source folder
source_root = Path("data/source_documents")

# Root output folder
output_root = Path("data/page_images")

# Find all PDFs recursively
pdf_files = source_root.rglob("*.pdf")

for pdf_path in pdf_files:

    # Example:
    # laws/law_01.pdf
    category = pdf_path.parent.name
    pdf_name = pdf_path.stem

    # Output folder
    output_dir = output_root / category / pdf_name

    output_dir.mkdir(parents=True, exist_ok=True)

    # Skip if already converted
    existing_images = list(output_dir.glob("*.png"))

    if existing_images:
        print(f"Skipping already processed: {pdf_name}")
        continue

    print(f"\nProcessing: {pdf_path}")

    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=300)

    # Save pages
    for i, page in enumerate(pages):

        page_path = output_dir / f"page_{i+1:03}.png"

        page.save(page_path, "PNG")

    print(f"Completed: {pdf_name}")

print("\nAll PDFs converted successfully.")