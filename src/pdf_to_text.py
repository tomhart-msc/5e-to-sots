import fitz
import textwrap
from tqdm import tqdm

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n\n".join([page.get_text() for page in tqdm(doc, desc="Extracting text")])

def chunk_text(text, max_chars=12000):
    chunks, current, count = [], [], 0
    for para in text.split("\n\n"):
        count += len(para)
        current.append(para)
        if count >= max_chars:
            chunks.append("\n\n".join(current))
            current, count = [], 0
    if current:
        chunks.append("\n\n".join(current))
    return chunks

def pdf_2_text(pdf_path):
    raw_text = extract_text(pdf_path)
    chunks = chunk_text(raw_text)
    adventure_text_chunks = []
    for i, chunk in enumerate(chunks):
        adventure_text_chunks.append(textwrap.indent(chunk.strip(), "    "))
    return "\n\n".join(adventure_text_chunks)