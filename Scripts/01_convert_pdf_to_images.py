from pdf2image import convert_from_path
from pathlib import Path

pdf_path = "data/source_documents/laws/law_01.pdf"

output_dir = Path("data/page_images/laws/law_01")
output_dir.mkdir(parents=True, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=300)

for i, page in enumerate(pages):
    page.save(output_dir / f"page_{i+1:03}.png", "PNG")

print("PDF converted successfully.")