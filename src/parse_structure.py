import yaml
from pathlib import Path

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip enclosing ```yaml and ``` if present
    if lines and lines[0].strip().startswith("```yaml"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    cleaned = "".join(lines)

    # Load all documents (returns a generator)
    docs = list(yaml.safe_load_all(cleaned))

    # Return a single doc or the whole list depending on how many documents exist
    return docs[0] if len(docs) == 1 else docs

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

