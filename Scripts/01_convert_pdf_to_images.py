from pdf2image import convert_from_path
from pathlib import Path

# Root source folder
source_root = Path("data/source_documents")

# Root output folder
output_root = Path("data/page_images")

# Find all PDFs recursively
pdf_files = source_root.rglob("*.pdf")

# Counters
processed_pdfs = 0
skipped_pdfs = 0
total_pages = 0

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
        skipped_pdfs += 1
        continue

    print(f"\nProcessing: {pdf_path}")

    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=300)

    # Save pages
    for i, page in enumerate(pages):

        page_path = output_dir / f"page_{i+1:03}.png"

        page.save(page_path, "PNG")

    page_count = len(pages)

    processed_pdfs += 1
    total_pages += page_count

    print(f"Completed: {pdf_name} ({page_count} pages)")

print("\n========== SUMMARY ==========")
print(f"Processed PDFs : {processed_pdfs}")
print(f"Skipped PDFs   : {skipped_pdfs}")
print(f"Total PNG pages: {total_pages}")
print("All PDFs converted successfully.")