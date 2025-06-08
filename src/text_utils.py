import fitz
import textwrap
from tqdm import tqdm
from pathlib import Path
import re

def strip_code_blocks(filename: str):
    """
    Removes lines containing "```" from the input file and
    saves the result back to the same filename. This version is
    more resilient to extra characters (like colons or spaces)
    before the code block markers.

    Args:
        filename (str): The path to the file to be processed.
    """
    try:
        with open(filename, 'r') as f_read:
            lines = f_read.readlines()

        # Check if the stripped line contains '```' anywhere
        filtered_lines = [line for line in lines if "```" not in line.strip()]

        with open(filename, 'w') as f_write:
            f_write.writelines(filtered_lines)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    # Keeping page numbers for better context if needed later
    return "\n\n".join([f"[PAGE {i+1}]\n{page.get_text()}" for i, page in enumerate(tqdm(doc, desc="Extracting text"))])

def chunk_text(text, max_chars=12000): # Ensure this handles chunks appropriately for LLM context window
    chunks, current, count = [], [], 0
    paragraphs = text.split("\n\n")
    for para in paragraphs:
        para_len = len(para) + 2 # +2 for the \n\n
        if count + para_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current, count = [], 0
        current.append(para)
        count += para_len
    if current:
        chunks.append("\n\n".join(current))
    return chunks

def extract_pdf_text(pdf_path: Path):
    raw_text = extract_text(pdf_path)
    chunks = chunk_text(raw_text)    
    # For simplicity, we'll combine all chunks for the prompt.
    # For very large PDFs, you might iterate and call LLM per chunk, then merge.
    return "\n\n".join([textwrap.indent(chunk.strip(), "    ") for chunk in chunks])

def extract_markdown_section(markdown_text: str, section_title: str, header_level: int = 2) -> str:
    """
    Extract a section from Markdown text based on the header title and level.
    
    Args:
        markdown_text: The full Markdown string.
        section_title: The section title to extract (e.g., "Plot Summary").
        header_level: The Markdown header level to match (e.g., 2 for ##).

    Returns:
        The content of the section as a string, or "" if not found.
    """
    header_pattern = r'^{} {}\s*$'.format('#' * header_level, re.escape(section_title))
    pattern = re.compile(header_pattern, re.MULTILINE)

    matches = list(pattern.finditer(markdown_text))
    if not matches:
        return ""

    start = matches[0].end()

    # Look for the next header of the same or higher level
    next_section = re.compile(r'^#{1,%d} .+' % header_level, re.MULTILINE)
    following_match = next_section.search(markdown_text, pos=start)

    end = following_match.start() if following_match else len(markdown_text)

    return markdown_text[start:end].strip()