import json
import shutil
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# File created by ingest.py.
# This file contains one JSON object per chunk.
CHUNKS_FILE = Path("data/chunks.jsonl")

# Folder where ChromaDB will save the local vector database.
CHROMA_DIR = Path("chroma_db")

# Name of the ChromaDB collection for this project.
COLLECTION_NAME = "professor_reviews"


def load_chunks():
    """
    Load all chunks from data/chunks.jsonl.

    Each line in the file is one JSON object with:
    - id
    - source
    - chunk_index
    - text
    """
    chunks = []

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {CHUNKS_FILE}. Run python ingest.py first."
        )

    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def main():
    """
    Build the vector index for Milestone 4.

    Steps:
    1. Load chunks from data/chunks.jsonl.
    2. Create embeddings using all-MiniLM-L6-v2.
    3. Store the chunks, embeddings, and metadata in ChromaDB.
    """
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.")

    # Rebuild the database from scratch each time.
    # This prevents old chunks from staying in the database after changes.
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    # Load the local embedding model from sentence-transformers.
    # This model does not require an API key.
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create a persistent local ChromaDB client.
    # The database files will be stored in the chroma_db folder.
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Create or get the collection where professor review chunks will be stored.
    collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

    # Prepare the data for ChromaDB.
    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]

    # Metadata is important because it lets us cite the source later.
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print("Creating embeddings...")

    # Convert each text chunk into a vector embedding.
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    print("Adding chunks to ChromaDB...")

    # Store the chunk IDs, text, embeddings, and metadata in ChromaDB.
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Indexed {len(chunks)} chunks into {CHROMA_DIR}.")
    print(f"Collection name: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()