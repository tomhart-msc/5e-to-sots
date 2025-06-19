from pathlib import Path
from src.lore_utils import get_lore_markdown as get_lore_markdown_from_file
from src.lore_utils import get_adversary_renaming_table_markdown as get_adversary_renaming_table_markdown_from_file

def _lore_file(adventure_name: str) -> Path:
    return Path(f"work/extract_lore_{adventure_name}_prompt.response.md")

def get_lore_markdown(adventure_name: str) -> str:
    return get_lore_markdown_from_file(_lore_file(adventure_name))

def get_adversary_renaming_table_markdown(adventure_name: Path) -> str:
    return get_adversary_renaming_table_markdown_from_file(_lore_file(adventure_name))
