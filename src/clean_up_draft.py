# src/clean_up_draft.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter
from src.notes import load_notes_md
import shutil
import os

def check_and_fallback_scenes(input_filename: str, output_filename: str):
    """
    Compares the number of lines starting with '## Scene' in two files.
    If the counts differ, it overwrites the output file with the content
    of the input file and prints a warning.

    Args:
        input_filename: The path to the original draft file.
        output_filename: The path to the LLM's output file.
    """

    def count_scene_lines(filename: str) -> int:
        """Helper to count '## Scene' lines."""
        count = 0
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('## Scene'):
                        count += 1
        except FileNotFoundError:
            print(f"Warning: File not found - {filename}")
            return -1  # Indicate an error
        return count

    input_scene_count = count_scene_lines(input_filename)
    output_scene_count = count_scene_lines(output_filename)

    if input_scene_count == -1 or output_scene_count == -1:
        # One or both files not found, warning already printed by helper.
        return

    if input_scene_count != output_scene_count:
        print(f"WARNING: Scene count mismatch!")
        print(f"  Input file ('{input_filename}') has {input_scene_count} scenes.")
        print(f"  Output file ('{output_filename}') has {output_scene_count} scenes.")
        try:
            shutil.copyfile(input_filename, output_filename)
            print(f"  Overwriting '{output_filename}' with content from '{input_filename}' (fallback initiated).")
        except Exception as e:
            print(f"  ERROR: Failed to overwrite output file: {e}")
    else:
        print(f"Scene count matched: {input_scene_count} scenes in both files. No fallback needed.")


def prompt_name(adventure_name: str):
    return f"clean_up_draft_{adventure_name}_prompt"

def response_path(adventure_name: str):
    """
    Returns the path to the raw LLM response file for the clean_up_draft step.
    """
    return Path("work") / f"clean_up_draft_{adventure_name}_prompt.response.md"

def run(draft: str, adventure_outline: str, dry_run: bool = False):
    """
    Runs the consistency check and introduction generation using an LLM.

    Args:
        draft_path (Path): Path to the combined draft markdown file.
        adventure_outline_path (Path): Path to the adventure outline markdown file.
        dry_run (bool): If True, generates prompt but does not call LLM.
    """
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    draft_path = Path(draft)
    adventure_outline_path = Path(adventure_outline)

    # Derive adventure_name from the draft_path (e.g., "golden-sun-tower_draft.md" -> "golden-sun-tower")
    adventure_name = draft_path.stem.replace("_draft", "")

    # Load shared references (assuming they are in data/ directory)
    try:
        rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
        system_reference = rules_reference # Renaming for consistency with templates
        setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Missing reference file. Ensure 'data/rules_reference.md' and 'data/setting_reference.md' exist. {e}")
        return None

    # Load raw content from input files
    try:
        raw_draft_content = draft_path.read_text(encoding="utf-8")
        raw_adventure_outline = adventure_outline_path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Could not read input files. {e}")
        return None

    adventure_notes_file = Path(f"notes/{adventure_name}_adventure_notes.md")
    adventure_gm_notes = load_notes_md(adventure_notes_file) if adventure_notes_file.exists() else {}
    lore_file = f"work/extract_lore_{adventure_name}_prompt.response.md"
    lore = Path(lore_file).read_text(encoding="utf-8")

    # Indent content to prevent markdown parsing issues with nested blocks
    # This ensures the content is treated as literal text within the prompt,
    # rather than as a nested code block.
    draft_content_indented = raw_draft_content.strip()
    adventure_outline_indented = raw_adventure_outline.strip()

    # Render Jinja2 template for the prompt
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("clean_up_draft_prompt.md.j2")
    prompt_content = template.render(
        lore=lore,
        system_reference=system_reference,
        setting_reference=setting_reference,
        adventure_gm_notes=adventure_gm_notes,
        # Pass the indented content to the template
        draft_content=draft_content_indented,
        adventure_outline=adventure_outline_indented
    )

    send_prompt_to_openrouter(prompt_md=prompt_content, prompt_name=prompt_name(adventure_name), dry_run=dry_run)
    if not dry_run:
        # Check if the LLM did anything crazy like dropping scenes. This conversion step is risky.
        # If it did, fall back to the input.
        input = draft_path
        output = response_path(adventure_name)
        check_and_fallback_scenes(input, output)
    
    return response_path(adventure_name) # Return the path to the LLM's raw response file