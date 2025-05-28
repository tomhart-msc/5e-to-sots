import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_notes_md(path):
    tone = None
    intent = ""
    allow_invention = False
    current_section = None
    sections = {"tone": "", "intent": "", "obstacles": "", "allow invention": ""}

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith("## "):
                current_section = line[3:].strip().lower()
            elif current_section:
                sections[current_section] += line + "\n"

    tone = sections["tone"].strip()
    intent = sections["intent"].strip()
    obstacles = sections["obstacles"].strip()
    allow_invention = "yes" in sections["allow invention"].lower()

    return {
        "tone": tone or None,
        "notes": intent or "",
        "obstacles": obstacles or None,
        "allow_invention": allow_invention
    }

def run(scene_path: str, adventure_outline_path: str, notes_path: str = None):
    scene_file = Path(scene_path)
    notes_file = Path(notes_path) if notes_path else None
    input_name = scene_file.stem.replace("scene_", "")
    output_path = Path("input") / f"scene_{input_name}_prompt.md"
    output_path.parent.mkdir(exist_ok=True)

    scene_data = load_yaml(scene_file)
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
        gm_notes=gm_notes,
        adventure_outline=adventure_outline,
        system_reference=rules_reference,
        setting_reference=setting_reference
    )

    output_path.write_text(prompt, encoding="utf-8")
    print(f"Prompt written to {output_path}")

