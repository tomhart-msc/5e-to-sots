import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter
from src.notes import load_notes_md
from src.convert_adversaries import response_path as convert_adversaries_response_path
from src.convert_magic_items_to_sorcerous_gear import response_path as convert_gear_path
from src.text_utils import extract_markdown_section
from src.yaml_utils import quote_colon_strings

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip enclosing ```yaml and ``` if present
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    cleaned = "".join(lines)
    return yaml.safe_load(quote_colon_strings(cleaned))

def prompt_path(scene_path: str):
    scene_file = Path(scene_path)
    input_name = scene_file.stem.replace("scene_", "").replace(".response", "")
    return f"scene_{input_name}_prompt"

def response_path(scene_path: str):
    work_dir = Path("work")
    return work_dir / f"{prompt_path(scene_path)}.response.md"

def run(scene_path: str, pdf_path: str, adventure_outline_path: str, notes_path: str = None, dry_run: bool = False):
    scene_file = Path(scene_path)
    notes_file = Path(notes_path) if notes_path else None
    pdf_file = Path(pdf_path)

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)
    
    adventure_name = pdf_file.stem
    adventure_notes_file = Path(f"notes/{adventure_name}_adventure_notes.md")
    lore_file = f"work/extract_lore_{adventure_name}_prompt.response.md"
    scene_data = load_yaml(scene_file)
    adventure_gm_notes = load_notes_md(adventure_notes_file) if adventure_notes_file.exists() else {}
    gm_notes = load_notes_md(notes_file) if notes_file and notes_file.exists() else {}
    adventure_outline = Path(adventure_outline_path).read_text(encoding="utf-8")
    lore = Path(lore_file).read_text(encoding="utf-8")

    # Load shared references
    rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
    setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")

    adversaries_markdown = Path(convert_adversaries_response_path(adventure_name)).read_text(encoding="utf-8")
    adversaries_table = extract_markdown_section(adversaries_markdown, "Renamed NPCs and Adversaries", 3)

    gear_markdown = Path(convert_gear_path(adventure_name)).read_text(encoding="utf-8")
    gear_table = extract_markdown_section(gear_markdown, "Transformed Magic Items", 3)

    # Render Jinja2 template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("scene_prompt.md.j2")
    prompt = template.render(
        gear_table=gear_table,
        adversaries_table = adversaries_table,
        lore=lore,
        scene=scene_data,
        adventure_gm_notes=adventure_gm_notes,
        gm_notes=gm_notes,
        adventure_outline=adventure_outline,
        system_reference=rules_reference,
        setting_reference=setting_reference
    )

    # Use the LLM helper to save prompt and optionally call OpenRouter
    send_prompt_to_openrouter(prompt_md=prompt, prompt_name=prompt_path(scene_path), dry_run=dry_run)
