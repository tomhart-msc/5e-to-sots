import os
from pathlib import Path
import sys
from openai import OpenAI 
import dotenv
import re
from typing import Optional, List

dotenv.load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)

WORK_DIR = Path("work")
WORK_DIR.mkdir(exist_ok=True)

MODEL="google/gemma-3-27b-it:free"

def extract_yaml_from_markdown(md_string: str) -> Optional[str]:
    """Extracts the first YAML block from a Markdown string."""
    match = re.search(r"```yaml\s*\n(.*?)\n```", md_string, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# LLMs are very bad about "slightly-off" output....
def extract_all_yaml_blocks_from_markdown(md_string: str) -> List[str]:
    """Extracts all YAML blocks from a Markdown string, even if some are unterminated."""
    blocks = []

    yaml_start_re = re.compile(r"```yaml\s*\n", re.IGNORECASE)
    generic_fence_re = re.compile(r"```")

    starts = [m.end() for m in yaml_start_re.finditer(md_string)]

    for i, start in enumerate(starts):
        # Find the next ```yaml or ``` after this start
        next_yaml = yaml_start_re.search(md_string, pos=start)
        next_close = generic_fence_re.search(md_string, pos=start)

        # Determine which comes first: next opening or next closing
        if next_yaml and (not next_close or next_yaml.start() < next_close.start()):
            end = next_yaml.start()
        elif next_close:
            end = next_close.start()
        else:
            end = len(md_string)  # No end found, take till the end

        block = md_string[start:end].strip()
        blocks.append(block)

    return blocks


def send_prompt_to_openrouter(prompt_md: str, prompt_name: str, dry_run: bool = False):
    """
    Save prompt markdown, send to OpenRouter unless dry_run,
    save and print response.
    
    - prompt_md: full prompt text to send
    - prompt_name: base filename without extension, used for work/*.md and work/*.response.md
    - dry_run: if True, skip API call and just write prompt file
    
    Returns the LLM response string (or None if dry_run).
    """
    prompt_path = WORK_DIR / f"{prompt_name}.md"
    response_path = WORK_DIR / f"{prompt_name}.response.md"

    # Save the prompt
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt_md)

    if dry_run:
        print(f"[dry-run] Prompt saved to {prompt_path}", file=sys.stderr)
        return None

    print(f"⏳ Sending request to OpenRouter {MODEL} model...", file=sys.stderr)

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt_md}
            ],
            # you can add extra_headers or extra_body if you want
        )
        response_text = completion.choices[0].message.content.strip()

        with open(response_path, "w", encoding="utf-8") as f:
            f.write(response_text)

        print(response_text)  # to stdout
        print(f"\n[response saved to {response_path}]", file=sys.stderr)

        return response_text

    except Exception as e:
        print(f"❌ Error calling OpenRouter API: {e}", file=sys.stderr)
        return None
