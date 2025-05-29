import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip enclosing ```yaml and ``` if present
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    cleaned = "".join(lines)
    return yaml.safe_load(cleaned)

def load_notes_md(path):
    tone = None
    intent = ""
    allow_invention = False
    current_section = None
    sections = {"tone": "", "notes": "", "obstacles": "", "allow invention": ""}

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith("## "):
                current_section = line[3:].strip().lower()
            elif current_section:
                sections[current_section] += line + "\n"

    tone = sections["tone"].strip()
    notes = sections["notes"].strip()
    obstacles = sections["obstacles"].strip()
    allow_invention = "yes" in sections["allow invention"].lower()

    return {
        "tone": tone or None,
        "notes": notes or "",
        "obstacles": obstacles or None,
        "allow_invention": allow_invention
    }

def prompt_path(scene_path: str):
    scene_file = Path(scene_path)
    input_name = scene_file.stem.replace("scene_", "").replace(".response", "")
    return f"scene_{input_name}_prompt"

def response_path(scene_path: str):
    work_dir = Path("work")
    return work_dir / f"{prompt_path(scene_path)}.response.md"

def run(scene_path: str, adventure_outline_path: str, notes_path: str = None, dry_run: bool = False):
    scene_file = Path(scene_path)
    notes_file = Path(notes_path) if notes_path else None
    
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)
    
    adventure_notes_file = Path("notes/adventure_notes.md")
    scene_data = load_yaml(scene_file)
    adventure_gm_notes = load_notes_md(adventure_notes_file) if adventure_notes_file.exists() else {}
    gm_notes = load_notes_md(notes_file) if notes_file and notes_file.exists() else {}
    adventure_outline = Path(adventure_outline_path).read_text(encoding="utf-8")

    # Load shared references
    rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
    setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")

    # Render Jinja2 template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("scene_prompt.md.j2")
    prompt = template.render(
        scene=scene_data,
        adventure_gm_notes=adventure_gm_notes,
        gm_notes=gm_notes,
        adventure_outline=adventure_outline,
        system_reference=rules_reference,
        setting_reference=setting_reference
    )

    # Use the LLM helper to save prompt and optionally call OpenRouter
    send_prompt_to_openrouter(prompt_md=prompt, prompt_name=prompt_path(scene_path), dry_run=dry_run)
