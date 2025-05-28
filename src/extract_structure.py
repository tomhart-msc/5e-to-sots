from pathlib import Path
import fitz
from tqdm import tqdm
import textwrap
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter

PROMPT_HEADER = """You are analyzing a Dungeons & Dragons 5E adventure module..."""  # truncated for clarity

def prompt_path(pdf_path: str):
    path = Path(pdf_path)
    input_name = path.stem
    return f"extract_structure_{input_name}_prompt"

def response_path(pdf_path: str):
    work_dir = Path("work")
    return work_dir / f"{prompt_path(pdf_path)}.response.md"

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
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    # Load shared references
    rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
    setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")

    raw_text = extract_text(pdf_path)
    chunks = chunk_text(raw_text)
    adventure_text_chunks = []
    for i, chunk in enumerate(chunks):
        adventure_text_chunks.append(textwrap.indent(chunk.strip(), "    "))
    adventure_text = "\n\n".join(adventure_text_chunks)

    # Render Jinja2 template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("outline_prompt.md.j2")
    prompt = template.render(
        adventure_text=adventure_text,
        system_reference=rules_reference,
        setting_reference=setting_reference
    )

    # Use the LLM helper to save prompt and optionally call OpenRouter
    send_prompt_to_openrouter(prompt_md=prompt, prompt_name=prompt_path(pdf_path), dry_run=dry_run)

