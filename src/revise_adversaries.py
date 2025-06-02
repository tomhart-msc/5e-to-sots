from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter

def prompt_name(adventure_name: str):
    return f"revise_adversaries_{adventure_name}_prompt"

def response_path(adventure_name: str):
    """
    Returns the path to the raw LLM response file for the revise_adversaries step.
    """
    return Path("work") / f"{prompt_name(adventure_name)}.response.md"

def strip_code_blocks(filename: str):
    """
    Removes lines starting with "```" from the input file and
    saves the result back to the same filename.

    Args:
        filename (str): The path to the file to be processed.
    """
    try:
        with open(filename, 'r') as f_read:
            lines = f_read.readlines()

        filtered_lines = [line for line in lines if not line.strip().startswith("```")]

        with open(filename, 'w') as f_write:
            f_write.writelines(filtered_lines)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run(pdf: str, draft: str, dry_run: bool = False):
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    pdf_path = Path(pdf)
    draft_path = Path(draft)
    adventure_name = pdf_path.stem

    # Load shared references (assuming they are in data/ directory)
    try:
        rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
        system_reference = rules_reference # Renaming for consistency with templates
        adversaries_reference = Path("data/adversaries_reference.md").read_text(encoding="utf-8")
        setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Missing reference file. Ensure 'data/adversaries_reference.md' and 'data/setting_reference.md' exist. {e}")
        return None

    # Load raw content from input files
    try:
        raw_draft_content = draft_path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Could not read input files. {e}")
        return None

    lore_file = f"work/extract_lore_{adventure_name}_prompt.response.md"
    lore = Path(lore_file).read_text(encoding="utf-8")

    draft_content_indented = raw_draft_content.strip()

    # Render Jinja2 template for the prompt
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("revise_adversaries_prompt.md.j2")
    prompt_content = template.render(
        lore=lore,
        system_reference=system_reference,
        adversaries_reference=adversaries_reference,
        setting_reference=setting_reference,
        draft_content=draft_content_indented
    )

    send_prompt_to_openrouter(prompt_md=prompt_content, prompt_name=prompt_name(adventure_name), dry_run=dry_run)
    
    # LLMs don't listen
    strip_code_blocks(response_path(adventure_name))