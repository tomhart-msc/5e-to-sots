from pathlib import Path
from jinja2 import Environment, FileSystemLoader

DATA_DIR = Path("data")
TEMPLATES_DIR = Path("templates")
INPUT_DIR = Path("input")


def load_file(path):
    if path == None:
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render_adventure_prompt(adventure_text, gm_notes, rules_reference, setting_reference):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("adventure_prompt.md.j2")
    return template.render(
        adventure_text=adventure_text,
        gm_notes=gm_notes,
        rules_reference=rules_reference,
        setting_reference=setting_reference,
    )


def run(adventure_path: str, notes_path: str = None):
    adventure_stem = Path(adventure_path).stem.replace("_structure", "")
    output_path = INPUT_DIR / f"{adventure_stem}_prompt.md"

    adventure_text = load_file(adventure_path)
    gm_notes = load_file(notes_path)
    rules_reference = load_file(DATA_DIR / "rules_reference.md")
    setting_reference = load_file(DATA_DIR / "setting_reference.md")

    prompt = render_adventure_prompt(adventure_text, gm_notes, rules_reference, setting_reference)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"Prompt written to {output_path}")