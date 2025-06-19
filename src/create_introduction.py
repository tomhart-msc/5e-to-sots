from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.notes import load_notes_md
from src.llm_utils import send_prompt_to_openrouter
from src.lore import get_lore_markdown

STEP_NAME="create_introduction"

def prompt_name(adventure_name: str):
    return f"{STEP_NAME}_{adventure_name}_prompt"

def response_path(adventure_name: str):
    """
    Returns the path to the raw LLM response file for the step.
    """
    return Path("work") / f"{prompt_name(adventure_name)}.response.md"

def run(pdf: str, draft: str, dry_run: bool = False):
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    pdf_path = Path(pdf)
    draft_path = Path(draft)
    adventure_name = pdf_path.stem

    # Load shared references (assuming they are in data/ directory)
    try:
        world_reference = Path("data/world_reference.md").read_text(encoding="utf-8")
        setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Missing reference file. Ensure 'data/adversaries_reference.md' and 'data/setting_reference.md' exist. {e}")
        return None

    # Load raw content from input files
    try:
        raw_draft_content = draft_path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Could not read input files. {e}")
        return None

    adventure_notes_file = Path(f"notes/{adventure_name}_adventure_notes.md")
    adventure_gm_notes = load_notes_md(adventure_notes_file) if adventure_notes_file.exists() else {}

    lore = get_lore_markdown(adventure_name)

    draft_content = raw_draft_content.strip()

    # Render Jinja2 template for the prompt
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(f"{STEP_NAME}_prompt.md.j2")
    prompt_content = template.render(
        adventure_gm_notes=adventure_gm_notes,
        lore=lore,
        world_reference=world_reference,
        setting_reference=setting_reference,
        draft_content=draft_content
    )

    send_prompt_to_openrouter(prompt_md=prompt_content, prompt_name=prompt_name(adventure_name), dry_run=dry_run)