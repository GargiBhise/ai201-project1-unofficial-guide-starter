import os
from dotenv import load_dotenv
from groq import Groq

from query import retrieve

# Load environment variables from .env
load_dotenv()

# Get the Groq API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"


def format_context(retrieved_chunks):
    """
    Format retrieved chunks into a context block for the LLM.

    Each chunk includes a source filename so the model can connect
    the answer back to the document.
    """
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']}, chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def get_unique_sources(retrieved_chunks):
    """Return a sorted list of unique source filenames."""
    return sorted(set(chunk["source"] for chunk in retrieved_chunks))


def ask(question: str, k: int = 5):
    """
    End-to-end RAG function.

    Steps:
    1. Retrieve relevant chunks from ChromaDB.
    2. Send those chunks to Groq as context.
    3. Generate a grounded answer.
    4. Return the answer and source list.
    """
    retrieved_chunks = retrieve(question, k=k)
    context = format_context(retrieved_chunks)
    sources = get_unique_sources(retrieved_chunks)

    system_prompt = """
You are answering questions about student reviews of Computer Science professors at Cal Poly Pomona.

Use ONLY the provided retrieved context.
Do not use outside knowledge.
Do not guess.
If the provided context does not contain enough information to answer the question, say:
"I don't have enough information in the provided reviews to answer that."

When you answer, mention the professor names only if they are supported by the context.
Keep the answer concise and grounded in the student reviews.
"""

    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}

Answer the question using only the retrieved context.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    # Programmatically append sources so attribution is guaranteed.
    answer_with_sources = (
        f"{answer}\n\n"
        f"Sources used: {', '.join(sources)}"
    )

    return {
        "answer": answer_with_sources,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


if __name__ == "__main__":
    test_questions = [
        "Which professor is most often described as having tough or test-heavy grading?",
        "Which professor do students praise for industry experience, career advice, mentorship, and practical assignments?",
        "What is the best parking lot at Cal Poly Pomona?",
    ]

    for question in test_questions:
        print("=" * 80)
        print(f"Question: {question}")
        print("=" * 80)

        result = ask(question)

        print(result["answer"])
        print()