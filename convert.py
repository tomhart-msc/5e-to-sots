import yaml
from jinja2 import Environment, FileSystemLoader
import argparse

# Load system reference block
SYSTEM_REFERENCE = """\
## SYSTEM REFERENCE: SWORDS OF THE SERPENTINE

You are generating content for *Swords of the Serpentine*, a sword & sorcery RPG based on the GUMSHOE system. Key principles:
- Investigative Abilities always succeed — never roll.
- General Abilities use 1d6 + spends vs. TN 4–8.
- Sorcery is illegal and corrupting.
- Sword & sorcery genre: gritty, personal, ancient powers, moral ambiguity.
- No D&D tropes: no XP, no random loot, no public monster fights.
"""

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def render_template(template_name, data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template.render(scene=data, system_reference=SYSTEM_REFERENCE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", help="Path to scene YAML", required=True)
    parser.add_argument("--template", default="scene_prompt.md.j2", help="Template filename")
    args = parser.parse_args()

    scene_data = load_yaml(args.scene)
    output = render_template(args.template, scene_data)
    print(output)

if __name__ == "__main__":
    main()

