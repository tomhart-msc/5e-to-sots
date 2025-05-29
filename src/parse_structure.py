import yaml
import re
from pathlib import Path

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip enclosing ```yaml and ``` if present
    if lines and lines[0].strip().startswith("```yaml"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    text = "".join(lines)

    # Split into individual scenes based on 'scene_number:' at the beginning of a line
    parts = re.split(r'(?=^scene_number:\s*\d+)', text, flags=re.MULTILINE)
    scenes = []

    for part in parts:
        part = part.strip()
        if not part:
            continue
        try:
            doc = yaml.safe_load(part)
            if isinstance(doc, dict):
                scenes.append(doc)
            else:
                print(f"[WARN] Skipped non-dict scene block")
        except Exception as e:
            print(f"[ERROR] Failed to parse scene:\n{part}\n{e}")
            continue

    return scenes

def run(structure_path):
    data = load_yaml(structure_path)
    scene_dir = Path("work")
    scene_dir.mkdir(exist_ok=True)

    for scene_data in data:
        idx = scene_data.get("scene_number")
        scene_filename = scene_dir / f"scene_{idx:02}.yaml"
        with open(scene_filename, "w", encoding="utf-8") as out_file:
            yaml.dump(scene_data, out_file, sort_keys=False)

        print(f"Wrote {scene_filename}")

