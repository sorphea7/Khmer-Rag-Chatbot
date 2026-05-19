# Khmer Insurance RAG Chatbot

## Project Structure

```text
khmer-chatbot/
│
├── scripts/
│   ├── 01_convert_pdf_to_images.py
│   ├── 02_extract_text_gemini.py
│   ├── 03_clean_text.py
│   ├── 04_chunk_text.py
│   ├── 05_generate_embeddings.py
│   ├── 06_test_retrieval.py
│   └── utils.py
│
├── data/
│   │
│   ├── source_documents/
│   │   ├── guidance/
│   │   ├── laws/
│   │   ├── prakas/
│   │   └── sub_decrees/
│   │
│   ├── page_images/
│   │   ├── guidance/
│   │   ├── laws/
│   │   ├── prakas/
│   │   └── sub_decrees/
│   │
│   ├── extracted_text/
│   │   │
│   │   ├── raw/
│   │   │   ├── guidance/
│   │   │   ├── laws/
│   │   │   ├── prakas/
│   │   │   └── sub_decrees/
│   │   │
│   │   └── cleaned/
│   │       ├── guidance/
│   │       ├── laws/
│   │       ├── prakas/
│   │       └── sub_decrees/
│   │
│   ├── chunked_documents/
│   │   ├── guidance/
│   │   ├── laws/
│   │   ├── prakas/
│   │   └── sub_decrees/
│   │
│   ├── embeddings/
│   │
│   └── evaluation/
│
├── vector_db/
│
├── notebooks/
│
├── logs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Folder Explanations

## `scripts/`

Contains all pipeline processing scripts.

### `01_convert_pdf_to_images.py`

Converts PDF pages into image files (`.png`) because all PDFs are treated as image-based documents for consistent Khmer extraction.

### `02_extract_text_gemini.py`

Uses Gemini Vision API to extract Khmer and English text from page images.

### `03_clean_text.py`

Cleans extracted OCR text:

* Unicode normalization
* remove repeated headers/footers
* remove OCR noise
* fix formatting

### `04_chunk_text.py`

Splits cleaned documents into smaller chunks for RAG retrieval while preserving legal sections and clauses.

### `05_generate_embeddings.py`

Creates embeddings from chunks and stores them into the vector database.

### `06_test_retrieval.py`

Tests retrieval quality using sample queries.

### `utils.py`

Helper functions shared across scripts.

---

# `data/`

Main data pipeline directory.

---

## `data/source_documents/`

Stores original downloaded PDFs from the ICR/IRC website.

Documents are categorized into:

* `laws/`
* `sub_decrees/`
* `prakas/`
* `guidance/`
* `aml_pf/`

These files should NEVER be modified.

---

## `data/page_images/`

Stores generated page images converted from PDFs.

Example:

```text
page_images/prakas/prakas_001/page_001.png
```

Used for:

* Gemini OCR extraction
* debugging extraction problems
* manual review

---

## `data/extracted_text/raw/`

Stores raw extracted text directly from Gemini.

No cleaning is applied here.

Purpose:

* preserve original OCR output
* debugging OCR mistakes
* reprocessing if needed

---

## `data/extracted_text/cleaned/`

Stores cleaned and normalized text.

Cleaning includes:

* Khmer Unicode normalization
* removing duplicated text
* formatting cleanup
* OCR noise removal

This is the version used for chunking.

---

## `data/chunked_documents/`

Stores chunked RAG-ready documents.

Each chunk should contain:

* chunk text
* document name
* category
* page number
* metadata

These chunks are later embedded into the vector database.

---

## `data/embeddings/`

Stores generated embeddings or intermediate embedding files.

---

## `data/evaluation/`

Contains evaluation datasets and retrieval testing results.

Examples:

* gold Q&A pairs
* retrieval benchmarks
* hallucination audit logs

---

# `vector_db/`

Stores vector database files (Qdrant, FAISS, ChromaDB, etc.).

Used for semantic retrieval during chatbot querying.

---

# `notebooks/`

Jupyter notebooks for:

* experiments
* testing OCR quality
* embedding comparison
* debugging

---

# `requirements.txt`

Python dependencies for the project.

Example:

* pymupdf
* pdf2image
* google-generativeai
* qdrant-client
* sentence-transformers

---

# `.gitignore`

Defines files/folders ignored by Git.

Usually excludes:

* generated images
* embeddings
* vector DB files
* environment secrets

---

# Pipeline Workflow

```text
PDF Documents
      ↓
Convert PDF Pages → Images
      ↓
Gemini OCR Extraction
      ↓
Clean Khmer Text
      ↓
Chunk Documents
      ↓
Generate Embeddings
      ↓
Store in Vector Database
      ↓
RAG Chatbot Retrieval
```

---

# Current Project Scope

This project currently focuses ONLY on:

* PDFs from ICR/IRC website
* Khmer legal and insurance documents
* image-first extraction pipeline
* Gemini Vision OCR

Document categories:

* Laws
* Sub Decrees
* Prakas
* Guidance

## Dataset Structure

This repository includes all source PDF documents inside the `data/source_documents/` directory with consistent folder placement and file naming conventions.

Only the original source documents are tracked in the repository.

Other directories such as:
- `page_images/`
- `extracted_text/`
- `chunked_documents/`
- `embeddings/`
- `vector_db/`

are generated locally by running the pipeline scripts.

Contributors can reproduce all generated data locally using the scripts provided in the `scripts/` directory.

This focused scope helps maintain:

* cleaner data
* more reliable retrieval
* easier evaluation
* manageable internship scope
