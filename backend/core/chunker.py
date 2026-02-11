from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 2000, chunk_overlap: int = 200) -> list[str]:
    """
    Splits a large transcript into smaller chunks for the vector database.
    The overlap ensures we don't cut off important context mid-sentence.
    """
    print(f"Chunking text of length {len(text)}...")
    
    # Recursive splitter tries to split by paragraphs first, then sentences, then words
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    chunks = splitter.split_text(text)
    print(f"Created {len(chunks)} chunks.")
    return chunks 
