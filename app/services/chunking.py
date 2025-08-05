import spacy
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

nlp = spacy.load("en_core_web_sm")

def semantic_chunking(text: str, max_words: int = 200) -> List[str]:
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    chunks, current_chunk, current_len = [], [], 0

    for sent in sentences:
        word_count = len(sent.split())
        if current_len + word_count <= max_words:
            current_chunk.append(sent)
            current_len += word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk, current_len = [sent], word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def recursive_split_chunking(text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        length_function=len,
        add_start_index=False
    )
    return splitter.split_text(text)
