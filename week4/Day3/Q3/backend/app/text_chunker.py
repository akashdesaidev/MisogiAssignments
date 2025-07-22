from typing import List
import re

def fixed_size_chunker(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks of fixed size with overlap
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        
        # If this is not the first chunk, include overlap
        if start > 0:
            start = start - overlap
            
        # If this is the last chunk, adjust end to text length
        if end >= text_length:
            chunks.append(text[start:])
            break
            
        # Find the last space before the end to avoid cutting words
        last_space = text.rfind(' ', start, end)
        if last_space != -1:
            end = last_space
            
        chunks.append(text[start:end])
        start = end

    return chunks

def sentence_chunker(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks by sentences, trying to keep chunks close to chunk_size
    """
    # Simple sentence splitting - can be improved with better regex or NLP
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            # Keep last sentence for overlap if needed
            current_chunk = [current_chunk[-1]] if overlap > 0 else []
            current_length = len(current_chunk[0]) if current_chunk else 0
            
        current_chunk.append(sentence)
        current_length += sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def paragraph_chunker(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks by paragraphs, combining small paragraphs and splitting large ones
    """
    # Split by double newline to identify paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        para_length = len(para)
        
        # If paragraph is too large, split it using fixed_size_chunker
        if para_length > chunk_size:
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_length = 0
            chunks.extend(fixed_size_chunker(para, chunk_size, overlap))
            continue
            
        if current_length + para_length > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_length = 0
            
        current_chunk.append(para)
        current_length += para_length
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def sliding_window_chunker(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text using a sliding window approach with fixed overlap
    """
    chunks = []
    start = 0
    stride = chunk_size - overlap
    
    while start < len(text):
        end = start + chunk_size
        
        if end >= len(text):
            chunks.append(text[start:])
            break
            
        # Find the last space before the end
        last_space = text.rfind(' ', start, end)
        if last_space != -1:
            end = last_space
            
        chunks.append(text[start:end])
        start += stride
    
    return chunks 