from pathlib import Path
import textwrap

PROMPT = """You are extracting adversary stat blocks from a Dungeons & Dragons 5E adventure.

Your task is to identify all monsters, unique enemies, or notable NPCs with stats from the input text, and output each as a structured YAML block. Include only adversaries that have mechanical relevance.

For each adversary, output a YAML block with:
- `name`
- `type` (e.g., fiend, humanoid, celestial)
- `challenge_rating`
- `hit_points`
- `armor_class`
- `abilities`: a dictionary of STR, DEX, CON, INT, WIS, CHA
- `special_traits`: short description of any special powers
- `actions`: key attacks or abilities used in combat

Do not invent missing details. If any information is not given in the input, omit the field.

Return only YAML. No explanations or preamble.
"""

def run(markdown_path: str, output_path: Path = None):
    md_path = Path(markdown_path)
    input_name = md_path.stem
    text = md_path.read_text(encoding="utf-8")

    prompt = [PROMPT, "\n\n### Adventure Text:\n\n", textwrap.indent(text.strip(), "    ")]

    if output_path is None:
        output_path = Path("input") / f"{input_name}_adversaries.md"
        output_path.parent.mkdir(exist_ok=True)

    output_path.write_text("\n\n".join(prompt), encoding="utf-8")
    print(f"Prompt written to {output_path}")
    print("Paste into the LLM of your choice to extract D&D stat blocks as YAML.")


