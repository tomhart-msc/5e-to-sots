import os
from pathlib import Path
import sys

from openai import OpenAI  # assuming you use openai python lib for OpenRouter
import dotenv

dotenv.load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)

WORK_DIR = Path("work")
WORK_DIR.mkdir(exist_ok=True)

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

    print(f"⏳ Sending request to OpenRouter Gemini model...", file=sys.stderr)

    try:
        completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
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
