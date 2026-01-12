import faiss
import numpy as np
import json
import sys

# Arguments:
# sys.argv[1] = index_path
# sys.argv[2] = embedding_dim
# sys.argv[3] = top_k

index_path = sys.argv[1]
dim = int(sys.argv[2])
top_k = int(sys.argv[3])

# Read raw float32 query vector from stdin
query_bytes = sys.stdin.buffer.read()
query = np.frombuffer(query_bytes, dtype="float32").reshape(1, dim)

# Load FAISS index
index = faiss.read_index(index_path)

# Search
D, I = index.search(query, top_k)

# Output result
print(json.dumps({
    "indices": I[0].tolist(),
    "scores": D[0].tolist()
}))
