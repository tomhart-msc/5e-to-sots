# src/extract_locations.py
from pathlib import Path
import fitz
from tqdm import tqdm
import textwrap
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter, extract_yaml_from_markdown # Ensure extract_yaml_from_markdown is in llm_utils.py
import yaml
import re # For safe file naming if needed, though not directly used here for output path

# Note: PROMPT_HEADER from original extract_structure.py is not used in this refactored version
# PROMPT_HEADER = """You are analyzing a Dungeons & Dragons 5E adventure module..."""

def prompt_name(pdf_path: str):
    path = Path(pdf_path)
    input_name = path.stem
    return f"extract_locations_{input_name}_prompt"

def response_path(pdf_path: str):
    work_dir = Path("work")
    return work_dir / f"{prompt_name(pdf_path)}.response.md"

def output_locations_path(pdf_path: str):
    work_dir = Path("work")
    return work_dir / f"{Path(pdf_path).stem}.locations.yaml" # Outputting identified locations here, named after adventure

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    # Keeping page numbers for better context if needed later
    return "\n\n".join([f"[PAGE {i+1}]\n{page.get_text()}" for i, page in enumerate(tqdm(doc, desc="Extracting text"))])

def chunk_text(text, max_chars=12000): # Ensure this handles chunks appropriately for LLM context window
    chunks, current, count = [], [], 0
    paragraphs = text.split("\n\n")
    for para in paragraphs:
        para_len = len(para) + 2 # +2 for the \n\n
        if count + para_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current, count = [], 0
        current.append(para)
        count += para_len
    if current:
        chunks.append("\n\n".join(current))
    return chunks

def run(pdf_path, dry_run: bool = False):
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
    setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")

    raw_text = extract_text(pdf_path)
    chunks = chunk_text(raw_text)
    
    # For simplicity, we'll combine all chunks for the prompt.
    # For very large PDFs, you might iterate and call LLM per chunk, then merge.
    adventure_text_for_prompt = "\n\n".join([textwrap.indent(chunk.strip(), "    ") for chunk in chunks])

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("extract_locations_prompt.md.j2") # NEW TEMPLATE
    prompt = template.render(
        adventure_text=adventure_text_for_prompt,
        system_reference=rules_reference,
        setting_reference=setting_reference
    )

    llm_response_md = send_prompt_to_openrouter(prompt_md=prompt, prompt_name=prompt_name(pdf_path), dry_run=dry_run)

    if not dry_run and llm_response_md:
        extracted_locations_yaml = extract_yaml_from_markdown(llm_response_md)
        if extracted_locations_yaml:
            output_path = output_locations_path(pdf_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(extracted_locations_yaml)
            print(f"Extracted locations saved to {output_path}")
        else:
            print("No YAML locations found in LLM response.")