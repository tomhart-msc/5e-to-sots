from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.text_utils import extract_pdf_text, strip_code_blocks
from src.llm_utils import send_prompt_to_openrouter

STEP_NAME="extract_adversaries"

def prompt_name(adventure_name: str):
    return f"{STEP_NAME}_{adventure_name}_prompt"

def response_path(adventure_name: str):
    """
    Returns the path to the raw LLM response file for the step.
    """
    return Path("work") / f"{prompt_name(adventure_name)}.response.md"

def run(pdf: str, dry_run: bool = False):
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    pdf_path = Path(pdf)
    adventure_name = pdf_path.stem

    # Render Jinja2 template for the prompt
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(f"{STEP_NAME}_prompt.md.j2")
    prompt_content = template.render(
        draft_content=extract_pdf_text(pdf_path)
    )

    send_prompt_to_openrouter(prompt_md=prompt_content, prompt_name=prompt_name(adventure_name), dry_run=dry_run)
    strip_code_blocks(response_path(adventure_name))
