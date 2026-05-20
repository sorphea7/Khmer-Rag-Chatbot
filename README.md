# Khmer Insurance RAG Chatbot

Khmer legal and insurance Retrieval-Augmented Generation (RAG) chatbot using:

* Gemini Vision OCR
* Khmer semantic retrieval
* FAISS vector search
* Streamlit frontend

This project processes Khmer legal PDFs into a searchable AI knowledge system.

---

# Current Features

* PDF → image conversion
* Khmer OCR extraction using Gemini
* Khmer text cleaning
* document chunking
* multilingual embeddings
* FAISS semantic retrieval
* Streamlit chatbot UI
* grounded RAG answering
* source inspection and retrieval debugging

---

# Tech Stack

* Python 3.11
* Gemini API
* Sentence Transformers
* FAISS
* Streamlit
* Pillow
* NumPy

---

# Project Structure

```text
khmer-chatbot/
│
├── Scripts/
│   ├── 01_convert_pdf_to_images.py
│   ├── 02_extract_text_gemini.py
│   ├── 03_clean_text.py
│   ├── 04_chunk_documents.py
│   └── 05_generate_embeddings.py
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
│   └── chunked_documents/
│       ├── guidance/
│       ├── laws/
│       ├── prakas/
│       └── sub_decrees/
│
├── vector_db/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
├── README.md
└── .venv
```

---

# Folder Explanations

## `Scripts/`

Contains the complete data processing pipeline.

---

## `01_convert_pdf_to_images.py`

Converts PDFs into page images (`.png`) for OCR processing.

Uses:

* `pdf2image`
* 400 DPI rendering for better Khmer OCR quality

---

## `02_extract_text_gemini.py`

Performs OCR extraction using Gemini Vision.

Features:

* Khmer + English extraction
* retry logic
* resumable processing
* automatic skip for completed pages
* strict OCR prompting

Output:

* raw JSON OCR files

---

## `03_clean_text.py`

Cleans OCR text while preserving Khmer legal structure.

Cleaning includes:

* whitespace normalization
* line break cleanup
* formatting cleanup

Minimal cleaning is intentionally used to avoid damaging Khmer legal text.

---

## `04_chunk_documents.py`

Splits cleaned text into smaller RAG chunks.

Features:

* Khmer-safe chunking
* paragraph-based splitting
* metadata preservation

Each chunk contains:

* document ID
* page number
* chunk ID
* text

---

## `05_generate_embeddings.py`

Generates multilingual embeddings and creates FAISS vector databases.

Uses:

* `paraphrase-multilingual-MiniLM-L12-v2`
* FAISS vector indexing

Output:

* `.index`
* metadata JSON

---

## `utils.py`

Stores shared helper functions used across multiple scripts.

This file is reserved for reusable utilities such as:

* retry handling
* JSON save/load helpers
* folder creation helpers
* runtime formatting
* OCR helper functions
* logging utilities

Utilities are added gradually as the project grows to avoid unnecessary early abstraction.

The goal of `utils.py` is to improve:

* code reusability
* maintainability
* cleaner pipeline scripts

---

# `data/`

Main project data directory.

---

## `data/source_documents/`

Stores original Khmer legal PDFs.

Categories:

* laws
* sub_decrees
* prakas
* guidance

These files should never be modified.

---

## `data/page_images/`

Stores generated page images.

Example:

```text
page_images/laws/law_01/page_001.png
```

Used for:

* OCR extraction
* debugging
* manual verification

---

## `data/extracted_text/raw/`

Stores raw OCR output from Gemini.

No cleaning is applied here.

Purpose:

* preserve original OCR
* OCR debugging
* reprocessing

---

## `data/extracted_text/cleaned/`

Stores cleaned OCR text.

This version is used for chunking and embeddings.

---

## `data/chunked_documents/`

Stores chunked RAG-ready documents.

Each file contains structured chunks with metadata.

---

# `vector_db/`

Stores FAISS vector databases and metadata.

Example:

```text
vector_db/
├── law_01.index
└── law_01_metadata.json
```

Used for:

* semantic retrieval
* RAG search
* chatbot grounding

---

# Environment Setup

## 1. Clone Repository

```bash
git clone git@github.com:sorphea7/Khmer-Rag-Insurance-Chatbot.git
cd khmer-chatbot
```

---

## 2. Create Virtual Environment

```bash
python3.11 -m venv .venv
```

---

## 3. Activate Virtual Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create `.env`

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

---

# Requirements

Current dependencies:

```text
streamlit
google-genai
python-dotenv
Pillow
sentence-transformers
faiss-cpu
numpy
torch
transformers
huggingface-hub
pdf2image
```

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
Store in FAISS Vector Database
      ↓
RAG Chatbot Retrieval
```

---

# Pipeline Execution Order

Run scripts in this exact order.

---

## Step 1 — Convert PDFs to Images

```bash
python Scripts/01_convert_pdf_to_images.py
```

---

## Step 2 — OCR Extraction

```bash
python Scripts/02_extract_text_gemini.py
```

This is the slowest stage because it uses Gemini Vision OCR.

Features:

* retry logic
* resumable processing
* skip completed pages

---

## Step 3 — Clean OCR Text

```bash
python Scripts/03_clean_text.py
```

---

## Step 4 — Chunk Documents

```bash
python Scripts/04_chunk_documents.py
```

---

## Step 5 — Generate Embeddings

```bash
python Scripts/05_generate_embeddings.py
```

---

# Run Chatbot UI

Start the Streamlit frontend:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

Features:

* Khmer question answering
* semantic retrieval
* retrieved source inspection
* grounded AI responses
* RAG debugging

---

# Current Scope

This project currently focuses only on:

* Khmer legal documents
* insurance regulations
* image-based PDFs
* Khmer semantic retrieval
* Gemini OCR pipeline

Document categories:

* Laws
* Sub Decrees
* Prakas
* Guidance

---

# Notes

* OCR quality depends heavily on PDF quality.
* 400 DPI is currently used for better Khmer OCR performance.
* Gemini Vision OCR is the primary bottleneck of the pipeline.
* Streamlit frontend replaces terminal-based retrieval testing.

---

# Future Improvements

Planned improvements:

* multi-document retrieval
* citation highlighting
* article-level chunking
* chat memory
* reranking
* OCR evaluation tools
* better Khmer embeddings
* production deployment
