#!/usr/bin/env python
import argparse
from src import extract_structure
from src import extract_locations, group_locations_to_scenes # New imports
from src import extract_adversaries
from src import convert_scene
from src import convert_adventure
from src import summarize_adventure
from src import clean_up_draft
from src import revise_adversaries
from src import extract_lore
from src import create_introduction
from src import create_conclusion
from src import convert_adversaries

def main():
    parser = argparse.ArgumentParser(description="Convert D&D 5e adventures into Swords of the Serpentine format.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # NEW: extract-lore
    parser_extract_lore = subparsers.add_parser("extract-lore", help="Extract lore from a PDF adventure and adapt to SOTS")
    parser_extract_lore.add_argument("--pdf", required=True, help="Path to PDF")
    parser_extract_lore.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    # extract-structure
    parser_extract = subparsers.add_parser("extract-structure", help="Extract adventure structure from a PDF")
    parser_extract.add_argument("--pdf", required=True, help="Path to PDF")
    parser_extract.add_argument("--output-prompt", action="store_true", help="Output a manual prompt for LLM use")
    parser_extract.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    # NEW: extract-locations
    parser_extract_locations = subparsers.add_parser("extract-locations", help="Extract distinct locations from a PDF adventure")
    parser_extract_locations.add_argument("--pdf", required=True, help="Path to PDF")
    parser_extract_locations.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    # NEW: group-scenes
    parser_group_scenes = subparsers.add_parser("group-scenes", help="Group identified locations into cohesive scene YAML files")
    parser_group_scenes.add_argument("--pdf", required=True, help="Path to the original PDF (for raw text context)")
    parser_group_scenes.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    parser_adversaries = subparsers.add_parser("extract-adversaries", help="Extract D&D stat blocks from adventure markdown")
    parser_adversaries.add_argument("--pdf", required=True, help="Path to the original PDF (for raw text context)")
    parser_adversaries.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    parser_convert_scene = subparsers.add_parser("convert-scene", help="Generate a scene conversion prompt")
    parser_convert_scene.add_argument("--scene", required=True, help="Path to scene YAML file (e.g., work/ADVENTURE_NAME_scenes/scene_01_*.yaml)")
    parser_convert_scene.add_argument("--pdf", required=True, help="Path to original PDF") # Changed to take PDF directly
    parser_convert_scene.add_argument("--adventure-outline", help="Path to adventure outline Markdown file (optional)")
    parser_convert_scene.add_argument("--notes", help="Path to GM notes Markdown file (optional)")
    parser_convert_scene.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    parser_convert_adventure = subparsers.add_parser("convert-adventure", help="Generate an adventure conversion prompt")
    parser_convert_adventure.add_argument("--adventure", required=True, help="Path to the adventure structure .md file")
    parser_convert_adventure.add_argument("--notes", required=False, help="Path to the GM notes .md file")
    parser_convert_adventure.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")
   
    parser_summarize_adventure = subparsers.add_parser("summarize-adventure", help="Generate a summarization prompt for an adventure")
    parser_summarize_adventure.add_argument("--pdf", required=True, help="Path to PDF") # Changed to take PDF directly
    parser_summarize_adventure.add_argument("--dry-run", action="store_true", help="Generate prompts but do not call LLM")

    # New subparser for the 'clean-up-draft' mode
    clean_up_draft_parser = subparsers.add_parser("clean-up-draft", help="Performs a final consistency check on the drafted adventure and writes an introduction.")
    clean_up_draft_parser.add_argument("--draft", required=True, help="Path to the combined draft markdown file.")
    clean_up_draft_parser.add_argument("--adventure-outline", required=True, help="Path to the adventure outline markdown file.")
    clean_up_draft_parser.add_argument("--dry-run", action="store_true", help="Generate prompt but do not call LLM.")

    revise_adversaries_parser = subparsers.add_parser("revise-adversaries", help="Cleans up the adversaries")
    revise_adversaries_parser.add_argument("--pdf", required=True, help="Path to original PDF") # Changed to take PDF directly
    revise_adversaries_parser.add_argument("--draft", required=True, help="Path to the combined draft markdown file.")
    revise_adversaries_parser.add_argument("--dry-run", action="store_true", help="Generate prompt but do not call LLM.")

    create_introduction_parser = subparsers.add_parser("create-introduction", help="Writes an introduction for the adventure")
    create_introduction_parser.add_argument("--pdf", required=True, help="Path to original PDF") # Changed to take PDF directly
    create_introduction_parser.add_argument("--draft", required=True, help="Path to the combined draft markdown file.")
    create_introduction_parser.add_argument("--dry-run", action="store_true", help="Generate prompt but do not call LLM.")

    create_conclusion_parser = subparsers.add_parser("create-conclusion", help="Writes a conclusion for the adventure")
    create_conclusion_parser.add_argument("--pdf", required=True, help="Path to original PDF") # Changed to take PDF directly
    create_conclusion_parser.add_argument("--draft", required=True, help="Path to the combined draft markdown file.")
    create_conclusion_parser.add_argument("--dry-run", action="store_true", help="Generate prompt but do not call LLM.")

    convert_adversaries_parser = subparsers.add_parser("convert-adversaries", help="Convert NPCs and adversaries for the adventure")
    convert_adversaries_parser.add_argument("--pdf", required=True, help="Path to original PDF") # Changed to take PDF directly
    convert_adversaries_parser.add_argument("--dry-run", action="store_true", help="Generate prompt but do not call LLM.")

    args = parser.parse_args()

    if args.command == "extract-lore":
        dry_run = args.dry_run
        extract_lore.run(pdf_path=args.pdf, dry_run=dry_run)
    elif args.command == "extract-structure":
        dry_run = args.dry_run
        extract_structure.run(pdf_path=args.pdf, dry_run=dry_run)
    elif args.command == "extract-locations":
        dry_run = args.dry_run
        extract_locations.run(pdf_path=args.pdf, dry_run=dry_run)
    elif args.command == "group-scenes":
        dry_run = args.dry_run
        group_locations_to_scenes.run(pdf_path=args.pdf, dry_run=dry_run)
    elif args.command == "extract-adversaries":
        dry_run = args.dry_run
        extract_adversaries.run(args.pdf, dry_run=dry_run)
    elif args.command == "convert-scene":
        dry_run = args.dry_run
        convert_scene.run(scene_path=args.scene, pdf_path=args.pdf, adventure_outline_path=args.adventure_outline, notes_path=args.notes, dry_run=dry_run)
    elif args.command == "convert-adventure":
        dry_run = args.dry_run
        convert_adventure.run(adventure_path=args.adventure, notes_path=args.notes)
    elif args.command == "summarize-adventure":
        dry_run = args.dry_run
        summarize_adventure.run(pdf_path=args.pdf, dry_run=dry_run) # Updated to pass pdf_path
    elif args.command == "clean-up-draft":
        clean_up_draft.run(args.draft, args.adventure_outline, args.dry_run)
    elif args.command == "revise-adversaries":
        dry_run = args.dry_run
        revise_adversaries.run(args.pdf, args.draft, dry_run=dry_run)
    elif args.command == "create-introduction":
        dry_run = args.dry_run
        create_introduction.run(args.pdf, args.draft, dry_run=dry_run)
    elif args.command == "create-conclusion":
        dry_run = args.dry_run
        create_conclusion.run(args.pdf, args.draft, dry_run=dry_run)
    elif args.command == "convert-adversaries":
        dry_run = args.dry_run
        convert_adversaries.run(args.pdf, dry_run=dry_run)
    else:
        parser.print_help()
        return 1
    
if __name__ == "__main__":
    main()