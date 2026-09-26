# Legal Insight Engine

A simple mini-project combining Deep Learning, Data Engineering, Data Security & Privacy, and Data Visualization.

## What it does
A new legal judgment is uploaded through a browser interface. The backend extracts and cleans its text, masks a few common PII patterns, creates a semantic embedding with a pretrained Sentence Transformer, and retrieves the most semantically similar judgments from the historical 1950–2024 reference collection. It also returns an extractive summary and key terms.

## Why this architecture
The frontend is plain HTML/CSS/JavaScript and the backend is FastAPI. There is no React, Node build system, database server, or complex cloud setup. This is intentional: it is easier to run, understand, explain and modify for a college mini-project.

## Subject mapping
- Deep Learning: pretrained `all-MiniLM-L6-v2` sentence embeddings.
- Data Engineering: PDF ingestion → text extraction → cleaning → structured index → embeddings.
- Security & Privacy: PDF validation, size limit, in-memory upload processing and basic PII masking.
- Data Visualization: reference-collection statistics shown in the UI.

## Setup
1. Open this folder in VS Code.
2. `python -m venv .venv`
3. `.venv\Scripts\activate`
4. `pip install -r requirements.txt`

## Build the index
Start small:
`python scripts\build_index.py --dataset "C:\YOUR\PATH\supreme_court_judgments" --limit 100`

The script intentionally indexes only 1950–2024. Do not add 2025 to the historical reference index if you want to use 2025 judgments as new test cases.

After testing, remove `--limit 100` to process the full historical collection. The full run can take substantial time.

## Run backend
`python -m uvicorn backend.app.main:app --reload --port 8000`

## Run frontend
Open another terminal:
`python scripts\serve_frontend.py`

Then open `http://127.0.0.1:5500`.

## Embedding concept
A sentence transformer maps text into a vector. For example, two legally related passages may map to vectors that are closer in vector space than unrelated passages. Because the vectors are normalized, their dot product is cosine similarity. The project compares the new-case vector with the stored historical vectors and returns the top matches.

## Limitations
This is an educational research assistant, not a legal decision system. Similarity is not legal equivalence and is not a recommendation. The summary is extractive, not a generated legal opinion. The PII layer is basic pattern masking, not complete anonymization. Scanned image-only PDFs may need OCR, which is not included in this version.

## Dataset
Uses the Supreme Court Judgments dataset (1950–2024) from Kaggle:
https://www.kaggle.com/datasets/adarshsingh0903/legal-dataset-sc-judgments-india-19502024asrt
