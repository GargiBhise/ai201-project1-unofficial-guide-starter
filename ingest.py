from pathlib import Path
import json
import re

# Folder where the raw professor review .txt files are stored.
RAW_DIR = Path("data/raw")

# Output file where all processed chunks will be saved.
# JSONL means "JSON Lines": one JSON object per line.
OUTPUT_FILE = Path("data/chunks.jsonl")


def clean_text(text: str) -> str:
    """
    Clean the raw copied text.

    My source files are already mostly cleaned, but this function removes
    common copied website artifacts and normalizes spacing.
    """
    # Replace common HTML entities that sometimes appear in copied text.
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&#39;", "'")
    text = text.replace("&quot;", '"')

    # Normalize Windows/Mac/Linux line endings into regular "\n".
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Strip extra spaces from the beginning and end of each line.
    lines = [line.strip() for line in text.split("\n")]

    # Remove repeated blank lines so the output is easier to read.
    cleaned_lines = []
    previous_blank = False

    for line in lines:
        if line == "":
            # Keep only one blank line in a row.
            if not previous_blank:
                cleaned_lines.append(line)
            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    return "\n".join(cleaned_lines).strip()


def split_reviews(text: str):
    """
    Split one professor document into review-based chunks.

    Each of my .txt files follows this general format:
    Professor: Name
    Department: ...
    School: ...

    Review 1:
    Course: ...
    Review Text: ...

    Review 2:
    ...

    Since each student review is already a complete opinion, the best chunk
    for this dataset is usually one full review.
    """
    # Pull out professor-level metadata so every chunk keeps its context.
    professor_match = re.search(r"Professor:\s*(.+)", text)
    department_match = re.search(r"Department:\s*(.+)", text)
    school_match = re.search(r"School:\s*(.+)", text)

    professor = professor_match.group(1).strip() if professor_match else "Unknown professor"
    department = department_match.group(1).strip() if department_match else "Unknown department"
    school = school_match.group(1).strip() if school_match else "Unknown school"

    # Split the document wherever a new review starts.
    # The lookahead (?=...) keeps "Review 1:" at the beginning of each chunk.
    parts = re.split(r"\n(?=Review\s+\d+:)", text)

    chunks = []

    for part in parts:
        part = part.strip()

        # Skip the summary/header section and only keep review sections.
        if not part.startswith("Review"):
            continue

        # Add professor metadata to each review chunk.
        # This prevents chunks from losing which professor they are about.
        chunk = (
            f"Professor: {professor}\n"
            f"Department: {department}\n"
            f"School: {school}\n\n"
            f"{part}"
        )

        chunks.append(chunk)

    return chunks


def split_long_chunk(chunk: str, max_chars: int = 700, overlap: int = 100):
    """
    Split unusually long reviews.

    Most reviews should stay as one chunk. If a review is very long,
    this splits it into smaller pieces with a small overlap so context
    is not completely lost between pieces.
    """
    if len(chunk) <= max_chars:
        return [chunk]

    chunks = []
    start = 0

    while start < len(chunk):
        end = start + max_chars
        piece = chunk[start:end].strip()

        # Avoid saving empty chunks.
        if piece:
            chunks.append(piece)

        # Move forward, keeping some overlap with the previous chunk.
        start += max_chars - overlap

    return chunks


def main():
    """
    Main pipeline for Milestone 3.

    Steps:
    1. Load all .txt files from data/raw.
    2. Clean each document.
    3. Split each document into review-based chunks.
    4. Save all chunks to data/chunks.jsonl.
    5. Print 5 sample chunks for manual inspection.
    """
    all_chunks = []

    # Make sure the raw data folder exists.
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Could not find folder: {RAW_DIR}")

    # Get all .txt files in data/raw.
    txt_files = sorted(RAW_DIR.glob("*.txt"))

    # Stop early if no documents were found.
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {RAW_DIR}")

    print(f"Found {len(txt_files)} raw documents.")

    # Process each professor review file.
    for path in txt_files:
    # Read the raw text from disk.
    # errors="replace" prevents the script from crashing if a file has Windows-style characters.
        raw_text = path.read_text(encoding="utf-8", errors="replace")

    # Clean copied text and spacing.
        cleaned_text = clean_text(raw_text)

        # Split into one chunk per review.
        review_chunks = split_reviews(cleaned_text)

        # Split only the chunks that are too long.
        # For this dataset, each review is already short and mostly self-contained.
# Keeping the full review together avoids cutting off professor/course context.
        final_chunks = review_chunks

        print(f"{path.name}: {len(final_chunks)} chunks")

        # Store each chunk with metadata.
        # This metadata will be useful later for retrieval and source attribution.
        for i, chunk in enumerate(final_chunks):
            all_chunks.append({
                "id": f"{path.stem}_{i}",
                "source": path.name,
                "chunk_index": i,
                "text": chunk
            })

    # Make sure the output folder exists.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save chunks as JSONL.
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\nSaved {len(all_chunks)} chunks to {OUTPUT_FILE}")

    # Print 5 chunks so I can manually check the output before embedding.
    print("\nFive sample chunks:")
    print("=" * 80)

    for chunk in all_chunks[:5]:
        print(f"ID: {chunk['id']}")
        print(f"Source: {chunk['source']}")
        print(chunk["text"])
        print("-" * 80)


if __name__ == "__main__":
    main()