#!/usr/bin/env python
import argparse
from src import extract_structure, parse_structure, extract_adversaries
from src import convert_scene
from src import convert_adventure
from src import summarize_adventure

def main():
    parser = argparse.ArgumentParser(description="Convert D&D 5e adventures into Swords of the Serpentine format.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # extract-structure
    parser_extract = subparsers.add_parser("extract-structure", help="Extract adventure structure from a PDF")
    parser_extract.add_argument("--pdf", required=True, help="Path to PDF")
    parser_extract.add_argument("--output-prompt", action="store_true", help="Output a manual prompt for LLM use")
    parser_extract.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    # parse-scenes
    parser_scenes = subparsers.add_parser("parse-scenes", help="Convert structure.yaml into scene_XX.yaml files")
    parser_scenes.add_argument("--structure", required=True, help="Path to structured YAML file")
    parser_scenes.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    parser_adversaries = subparsers.add_parser("extract-adversaries", help="Extract D&D stat blocks from adventure markdown")
    parser_adversaries.add_argument("--markdown", required=True, help="Path to adventure .md")
    parser_adversaries.add_argument("--output-prompt", action="store_true", help="Output prompt for LLM")
    parser_adversaries.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    parser_convert_scene = subparsers.add_parser("convert-scene", help="Generate a scene conversion prompt")
    parser_convert_scene.add_argument("--scene", required=True, help="Path to scene YAML file")
    parser_convert_scene.add_argument("--adventure-outline", help="Path to adventure outline Markdown file")
    parser_convert_scene.add_argument("--notes", help="Path to GM notes Markdown file")
    parser_convert_scene.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    parser_convert_adventure = subparsers.add_parser("convert-adventure", help="Generate an adventure conversion prompt")
    parser_convert_adventure.add_argument("--adventure", required=True, help="Path to the adventure structure .md file")
    parser_convert_adventure.add_argument("--notes", required=False, help="Path to the GM notes .md file")
    parser_convert_adventure.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")
   
    parser_summarize_adventure = subparsers.add_parser("summarize-adventure", help="Generate a summarization prompt for an adventure")
    parser_summarize_adventure.add_argument("--adventure", required=True, help="Path to the adventure structure .md file")
    parser_summarize_adventure.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    args = parser.parse_args()
    dry_run = args.dry_run

    if args.command == "extract-structure":
        extract_structure.run(pdf_path=args.pdf, dry_run=dry_run)
    elif args.command == "parse-scenes":
        parse_structure.run(structure_path=args.structure)
    elif args.command == "extract-adversaries":
        extract_adversaries.run(markdown_path=args.markdown)
    elif args.command == "convert-scene":
        convert_scene.run(scene_path=args.scene, adventure_outline_path=args.adventure_outline, notes_path=args.notes, dry_run=dry_run)
    elif args.command == "convert-adventure":
        convert_adventure.run(adventure_path=args.adventure, notes_path=args.notes)
    elif args.command == "summarize-adventure":
        summarize_adventure.run(adventure_path=args.adventure, dry_run=dry_run)

if __name__ == "__main__":
    main()

