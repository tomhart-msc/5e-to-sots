from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.notes import load_notes_md
from src.llm_utils import send_prompt_to_openrouter
from src.extract_magic_items import response_path as extract_magic_items_path
from src.text_utils import extract_pdf_text, strip_code_blocks, extract_markdown_section

STEP_NAME="convert_magic_items_to_sorcerous_gear"

def prompt_name(adventure_name: str):
    return f"{STEP_NAME}_{adventure_name}_prompt"

def response_path(adventure_name: str):
    """
    Returns the path to the raw LLM response file for the step.
    """
    return Path("work") / f"{prompt_name(adventure_name)}.response.md"

def create_gear_section(markdown_file, adventure_name):
    gear_section_file = f"work/{adventure_name}_gear_appendix.md"

    # Read the full markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f_read:
        markdown_text = f_read.read()

    # Extract the "Adversary Statistics" section
    gear_section = extract_markdown_section(markdown_text, "Gear Descriptions", 3)

    # Write the extracted section to the new file
    print (f"writing to {gear_section_file}")
    with open(gear_section_file, 'w', encoding='utf-8') as f_write:
        f_write.write("## Appendix: Gear\n\n")
        f_write.write(gear_section + '\n')

def run(pdf: str, dry_run: bool = False):
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    pdf_path = Path(pdf)
    adventure_name = pdf_path.stem

    magic_items_yaml_path = extract_magic_items_path(adventure_name)
    magic_items_yaml = Path(magic_items_yaml_path).read_text(encoding="utf-8")

    # Load shared references (assuming they are in data/ directory)
    try:
        system_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
        setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")
        sorcerous_gear_reference = Path("data/sorcerous_gear_reference.md").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Missing reference file. {e}")
        return None

    lore_file = f"work/extract_lore_{adventure_name}_prompt.response.md"
    lore = Path(lore_file).read_text(encoding="utf-8")

    adventure_notes_file = Path(f"notes/{adventure_name}_adventure_notes.md")
    adventure_gm_notes = load_notes_md(adventure_notes_file) if adventure_notes_file.exists() else {}

    # Render Jinja2 template for the prompt
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(f"{STEP_NAME}_prompt.md.j2")
    prompt_content = template.render(
        adventure_gm_notes=adventure_gm_notes,
        lore=lore,
        system_reference=system_reference,
        sorcerous_gear_reference=sorcerous_gear_reference,
        setting_reference=setting_reference,
        magic_items=magic_items_yaml,
        draft_content=extract_pdf_text(pdf_path)
    )

    send_prompt_to_openrouter(prompt_md=prompt_content, prompt_name=prompt_name(adventure_name), dry_run=dry_run)
    if not dry_run:
        strip_code_blocks(response_path(adventure_name))
        # Process the statistics into an adventure appendix
        create_gear_section(response_path(adventure_name), adventure_name)