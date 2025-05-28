import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter
from src.pdf_to_text import pdf_2_text

def prompt_path(adventure_path: str):
    input_name = Path(adventure_path).stem
    return f"{input_name}_summary_prompt"

def response_path(adventure_path: str):
    work_dir = Path("work")
    return work_dir / f"{prompt_path(adventure_path)}.response.md"

def run(adventure_path: str, dry_run: bool = False):
    input_path = Path(adventure_path)
    if not input_path.exists():
        print(f"Error: {adventure_path} not found.")
        sys.exit(1)

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    adventure_text = pdf_2_text(input_path)

    # Set up Jinja2 environment and load prompt template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('summarize_adventure_prompt.md.j2')

    # Render the prompt with the adventure text injected
    prompt= template.render(adventure_text=adventure_text)

    # Use the LLM helper to save prompt and optionally call OpenRouter
    send_prompt_to_openrouter(prompt_md=prompt, prompt_name=prompt_path(adventure_path), dry_run=dry_run)