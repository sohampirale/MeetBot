import faiss
import numpy as np

DIM = 1024  # embedding dim

vectors = np.fromfile(
    "sessions/faiss_data/sessions.faiss",
    dtype="float32"
).reshape(-1, DIM)

index = faiss.IndexFlatIP(DIM)
index.add(vectors)

faiss.write_index(index, "sessions/faiss_data/sessions.index")
