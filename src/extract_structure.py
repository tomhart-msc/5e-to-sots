from pathlib import Path
import fitz
from tqdm import tqdm
import textwrap
from src.llm_utils import send_prompt_to_openrouter

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

def run(pdf_path, dry_run: bool = False):
    input_name = Path(pdf_path).stem

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    raw_text = extract_text(pdf_path)
    chunks = chunk_text(raw_text)

    full_prompt = [PROMPT_HEADER]
    for i, chunk in enumerate(chunks):
        full_prompt.append(f"\n\n### PDF Text Chunk {i + 1}:\n\n")
        full_prompt.append(textwrap.indent(chunk.strip(), "    "))
    prompt = "\n\n".join(full_prompt)

    # Use the LLM helper to save prompt and optionally call OpenRouter
    send_prompt_to_openrouter(prompt_md=prompt, prompt_name=f"extract_structure_{input_name}_prompt", dry_run=dry_run)

