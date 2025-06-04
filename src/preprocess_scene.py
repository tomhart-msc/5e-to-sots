import re
from typing import Dict


def parse_adversary_table(markdown_table: str) -> Dict[str, str]:
    """
    Parses a markdown adversary table into a dict mapping original names to revised names.

    Args:
        markdown_table: Markdown table string with headers: 'Original Name | Revised Name | Type'

    Returns:
        A dictionary {original_name: revised_name}
    """
    lines = markdown_table.strip().splitlines()
    entries = [line.strip() for line in lines if '|' in line and not line.startswith('|---')]

    replacements = {}
    for line in entries[1:]:  # Skip header row
        parts = [part.strip() for part in line.strip('|').split('|')]
        if len(parts) >= 2:
            original, revised = parts[:2]
            if original and revised:
                replacements[original] = revised
    return replacements


def rename_entities(text: str, name_map: Dict[str, str]) -> str:
    """
    Replaces all occurrences of entity names (including variants like 'the Apostate', 'Apostates')
    based on the name_map. Case-insensitive and word-boundary aware.

    Args:
        text: Scene markdown.
        name_map: Dict mapping {original_name: new_name}

    Returns:
        Text with all entity names replaced.
    """
    for old_name, new_name in name_map.items():
        # Handle word components (e.g. "Gilded Apostate" → ["Gilded", "Apostate"])
        words = old_name.split()
        if not words:
            continue

        # Common variants: the full name, with/without "the", and plural forms
        variants = {
            rf'\b{re.escape(old_name)}\b',                         # exact match
            rf'\bthe {re.escape(old_name)}\b',                     # "the Gilded Apostate"
            rf'\b{re.escape(words[-1])}s\b',                       # "Apostates"
            rf'\bthe {re.escape(words[-1])}s\b',                   # "the Apostates"
            rf'\b{re.escape(words[-1])}\b',                        # "Apostate" (last word only)
            rf'\bthe {re.escape(words[-1])}\b',                    # "the Apostate"
        }

        for pattern in variants:
            regex = re.compile(pattern, flags=re.IGNORECASE)
            text = regex.sub(new_name, text)

    return text


def strip_stat_blocks(text: str, original_names: Dict[str, str]) -> str:
    """
    Removes stat block-like sections from the text if they follow adversary names.

    Args:
        text: Full scene text.
        original_names: Keys from the adversary replacement dict.

    Returns:
        Text with stat blocks stripped or replaced.
    """
    for name in original_names:
        # Try to match headings or lines starting with the adversary name followed by newlines + D&D-like blocks
        pattern = re.compile(
            rf'(?:^|\n)\s*(\*\*\s*)?(The\s+)?{re.escape(name)}(?:\s*\*\*)?\s*\n(?:.|\n)*?(?:Armor Class|Hit Points|Challenge|STR\s|\n\n)',
            flags=re.IGNORECASE
        )
        text = pattern.sub(f"\n\n[Stat block for {original_names[name]} removed — describe the adversary narratively.]\n\n", text)

    return text


def preprocess_scene_text(scene_text: str, adversary_table_markdown: str) -> str:
    """
    Preprocesses the scene content by renaming adversaries and stripping stat blocks.

    Args:
        scene_text: Full scene Markdown text.
        adversary_table_markdown: Markdown table string listing old and new names.

    Returns:
        Cleaned Markdown scene string.
    """
    name_map = parse_adversary_table(adversary_table_markdown)
    text = rename_entities(scene_text, name_map)
    text = strip_stat_blocks(text, name_map)
    return text
