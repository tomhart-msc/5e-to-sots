#!/usr/bin/env python3
import os
import subprocess
import argparse
import sys
from pathlib import Path
import importlib.util
import pathlib
import inspect

def import_response_path_functions(src_dir="src"):
    response_funcs = {}
    src_path = pathlib.Path(src_dir)

    for py_file in src_path.glob("*.py"):
        module_name = py_file.stem
        module_path = py_file.resolve()

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            # Check if the module defines `response_path`
            func = getattr(mod, "response_path", None)
            if callable(func):
                response_funcs[module_name] = func

    return response_funcs

def run_cmd(args):
    print("Running:", " ".join(str(arg) for arg in args))
    subprocess.run(args, check=True)

def main():
    response_funcs = import_response_path_functions()
    parser = argparse.ArgumentParser(description="Convert a 5E adventure PDF into Swords of the Serpentine format.")
    parser.add_argument("--pdf", required=True, help="Path to the input adventure PDF")
    parser.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")
    args = parser.parse_args()

    input_pdf = Path(args.pdf)
    if not input_pdf.exists():
        print(f"Error: PDF not found at {input_pdf}")
        return 1

    # Step 1: Extract structure
    structure_md = response_funcs["extract_structure"](input_pdf)
    if not structure_md.exists():
        run_cmd(["./convert.py", "extract-structure", "--pdf", str(input_pdf)] + (["--dry-run"] if args.dry_run else []))

    if not structure_md.exists():
        print(f"Error: {structure_md} not found.")
        return 1

    # Step 2: Summarize adventure
    summary_md = response_funcs["summarize_adventure"](input_pdf)
    if not summary_md.exists():
        run_cmd(["./convert.py", "summarize-adventure", "--adventure", str(input_pdf)] + (["--dry-run"] if args.dry_run else []))

    if not summary_md.exists():
        print(f"Error: {summary_md} not found.")
        return 1

    # Step 3: Parse scenes
    run_cmd(["./convert.py", "parse-scenes", "--structure", str(structure_md)])

    # Step 4: Convert each scene
    scene_dir = Path("work")
    notes_dir = Path("notes")
    for scene_file in sorted(scene_dir.glob("scene_*.yaml")):
        scene_name = scene_file.stem  # e.g., "scene_03"
        notes_file = notes_dir / f"{scene_name}_notes.md"
        scene_summary_md = response_funcs["convert_scene"](scene_file)
        if not scene_summary_md.exists():
            cmd = ["./convert.py", "convert-scene", "--scene", str(scene_file), "--adventure-outline", str(summary_md)]
            if notes_file.exists():
                cmd += ["--notes", str(notes_file)]
            if args.dry_run:
                cmd += ["--dry-run"]
            run_cmd(cmd)

    # Step 5: Combine all output scene files and generate PDF
    output_files = sorted(Path("work").glob("scene_*_prompt.response.md"))
    combined_md = Path("work/converted_adventure.md")
    with open(combined_md, "w") as outfile:
        for file in output_files:
            with open(file, "r") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")

    pdf_output = Path("work/converted_adventure.pdf")
    run_cmd(["pandoc", str(combined_md), "-o", str(pdf_output), "--pdf-engine", "weasyprint"])
    print(f"PDF created at {pdf_output}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
