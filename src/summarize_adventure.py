import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def run(adventure_path: str):
    input_path = Path(adventure_path)
    if not input_path.exists():
        print(f"Error: {adventure_path} not found.")
        sys.exit(1)

    # Read in the full adventure structure markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        adventure_text = f.read()

    # Set up Jinja2 environment and load prompt template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('summarize_adventure_prompt.md.j2')

    # Render the prompt with the adventure text injected
    prompt_text = template.render(adventure_text=adventure_text)

    # Output prompt file to same folder as input
    output_path = Path("input") / input_path.name.replace("_structure.md", "_summary_prompt.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prompt_text)

    print(f"Prompt written to {output_path}")
