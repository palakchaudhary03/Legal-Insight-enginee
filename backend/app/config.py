from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PROCESSED=ROOT/"data"/"processed"
INDEX=PROCESSED/"case_index.csv"
EMBEDDINGS=PROCESSED/"embeddings.npy"
MODEL="all-MiniLM-L6-v2"
MAX_MB=10
