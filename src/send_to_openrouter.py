# src/send_to_openrouter.py

import sys
import os
import openai
from dotenv import load_dotenv

def main():
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Missing OPENROUTER_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    # Check for prompt via stdin
    if sys.stdin.isatty():
        print("❌ No prompt provided via stdin.", file=sys.stderr)
        sys.exit(1)

    prompt_text = sys.stdin.read().strip()
    if not prompt_text:
        print("❌ Empty prompt provided.", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI-compatible client
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    try:
        print("⏳ Sending request to OpenRouter model...", file=sys.stderr)
        completion = client.chat.completions.create(
            # Terrible for this use case
            #model="mistralai/mistral-nemo:free",
            # Empty output
            #model="google/gemma-2-9b-it:free",
            # 404 no endpoints found
            #model="google/gemini-2.5-pro-exp-03-25",
            # Output is utter garbage
            #model="google/gemma-3-1b-it:free",
            model="google/gemma-3-27b-it:free",
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",  # Optional: can be your project or repo
                "X-Title": "5e-to-sots",             # Optional: app/project name
            }
        )

        print("✅ Response received from Gemini", file=sys.stderr)
        print(completion.choices[0].message.content)

    except Exception as e:
        print(f"❌ Error calling OpenRouter API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
