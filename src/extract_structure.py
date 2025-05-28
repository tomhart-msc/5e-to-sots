from pathlib import Path
import fitz
from tqdm import tqdm
import textwrap

PROMPT_HEADER = """You are analyzing a Dungeons & Dragons 5E adventure module..."""  # truncated for clarity

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

def run(pdf_path, output_prompt=False):
    input_name = Path(pdf_path).stem
    output_path = Path("input") / f"{input_name}_structure.md"
    output_path.parent.mkdir(exist_ok=True)

    raw_text = extract_text(pdf_path)
    chunks = chunk_text(raw_text)

    if output_prompt:
        full_prompt = [PROMPT_HEADER]
        for i, chunk in enumerate(chunks):
            full_prompt.append(f"\n\n### PDF Text Chunk {i + 1}:\n\n")
            full_prompt.append(textwrap.indent(chunk.strip(), "    "))
        output_path.write_text("\n\n".join(full_prompt), encoding="utf-8")
        print(f"Prompt written to {output_path}")
        print("Please paste this prompt into the LLM of your choice.")


