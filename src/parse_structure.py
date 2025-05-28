import yaml
from pathlib import Path

def run(structure_path):
    with open(structure_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    adventure_title = data.get("adventure_title", "Untitled Adventure")
    sections = data.get("sections", [])
    scene_dir = Path("scenes")
    scene_dir.mkdir(exist_ok=True)

    for idx, section in enumerate(sections, start=1):
        scene_data = {
            "scene_number": idx,
            "scene_title": section.get("title", f"Scene {idx}"),
            "source_section": section.get("title"),
            "purpose": section.get("summary", ""),
            "location": "",
            "content_excerpt": section.get("content_excerpt", "").strip(),
            "potential_adversaries": [],
        }

        scene_filename = scene_dir / f"scene_{idx:02}.yaml"
        with open(scene_filename, "w", encoding="utf-8") as out_file:
            yaml.dump(scene_data, out_file, sort_keys=False)

        print(f"Wrote {scene_filename}")

