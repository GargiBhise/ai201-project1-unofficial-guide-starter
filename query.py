import chromadb
from sentence_transformers import SentenceTransformer

# Folder where build_index.py saved the ChromaDB vector database.
CHROMA_DIR = "chroma_db"

# Must match the collection name used in build_index.py.
COLLECTION_NAME = "professor_reviews"

# Load the same embedding model used to build the index.
# The query must be embedded into the same vector space as the chunks.
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the local ChromaDB database.
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Load the professor review collection.
collection = client.get_collection(name=COLLECTION_NAME)


def retrieve(query: str, k: int = 5):
    """
    Retrieve the top-k chunks most relevant to the user query.

    Args:
        query: The user's search question.
        k: Number of chunks to retrieve.

    Returns:
        A list of dictionaries containing:
        - text
        - source
        - chunk_index
        - distance
    """
    # Convert the user query into an embedding.
    query_embedding = model.encode([query]).tolist()[0]

    # Ask ChromaDB for the closest chunks to the query embedding.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    # ChromaDB returns nested lists because it supports multiple queries at once.
    # Since we only send one query, we use index [0].
    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append(
            {
                "text": doc,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )

    return retrieved


def print_results(query: str, k: int = 5):
    """
    Print retrieval results in a readable format.

    This is mainly for Milestone 4 testing and README evidence.
    """
    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)

    results = retrieve(query, k=k)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Source: {result['source']}")
        print(f"Chunk index: {result['chunk_index']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["text"])
        print("-" * 80)


if __name__ == "__main__":
    # These are 3 questions from the evaluation plan in planning.md.
    # They help check whether retrieval works before adding the LLM.
    test_queries = [
    "Which professor is most often described as having tough or test-heavy grading?",
    "Which professor do students praise for industry experience, career advice, mentorship, and practical assignments?",
    "Which professor is commonly described as easy, chill, or lenient?",
    ]

    # Print the top 5 chunks for each test query.
    for query in test_queries:
        print_results(query, k=5)