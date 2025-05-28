import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter

def run(adventure_path: str, dry_run: bool = False):
    input_path = Path(adventure_path)
    if not input_path.exists():
        print(f"Error: {adventure_path} not found.")
        sys.exit(1)

    print("❌ Warning: output will likely be truncated due to size", file=sys.stderr)

    input_name = Path(adventure_path).stem

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    # Read in the full adventure structure markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        adventure_text = f.read()

    # Set up Jinja2 environment and load prompt template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('summarize_adventure_prompt.md.j2')

    # Render the prompt with the adventure text injected
    prompt= template.render(adventure_text=adventure_text)

    # Use the LLM helper to save prompt and optionally call OpenRouter
    send_prompt_to_openrouter(prompt_md=prompt, prompt_name=input_name.replace("_structure", "_summary_prompt"), dry_run=dry_run)