from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.llm_utils import send_prompt_to_openrouter, extract_all_yaml_blocks_from_markdown
from src.yaml_utils import quote_colon_strings
import yaml
import textwrap
import re
from typing import List, Dict, Any

def prompt_path(pdf_path: str):
    path = Path(pdf_path)
    input_name = path.stem
    return f"group_locations_to_scenes_{input_name}_prompt"

def response_path(pdf_path: str):
    path = Path(pdf_path)
    adventure_name = path.stem
    work_dir = Path("work")
    return work_dir / f"{prompt_path(adventure_name)}.response.md"

def output_scenes_dir(adventure_name: str):
    work_dir = Path("work")
    scenes_dir = work_dir / f"{adventure_name}_scenes"
    scenes_dir.mkdir(exist_ok=True)
    return scenes_dir

def apply_manual_grouping(adventure_name: str) -> Path:
    """
    Applies manual grouping instructions from notes/location_grouping_notes.md
    to the extracted locations YAML, creating a new processed locations YAML.
    """
    work_dir = Path("work")
    
    original_locations_path = work_dir / f"{adventure_name}.locations.yaml"
    if not original_locations_path.exists():
        raise FileNotFoundError(f"Original locations file not found at {original_locations_path}. Please run 'extract-locations' command first.")

    manual_notes_path = Path("notes/location_grouping_notes.md")
    
    # Load original locations
    with open(original_locations_path, "r", encoding="utf-8") as f:
        locations_data = yaml.safe_load(f)
    
    if not locations_data or 'locations' not in locations_data:
        print(f"Warning: No 'locations' key found in {original_locations_path}. Returning original path.")
        return original_locations_path

    current_locations: List[Dict[str, Any]] = locations_data['locations']
    
    # Process manual grouping notes
    if manual_notes_path.exists():
        print(f"Applying manual grouping instructions from {manual_notes_path}...")
        notes_content = manual_notes_path.read_text(encoding="utf-8")
        
        # Regex to find "Combine: A, B, C" lines
        combine_pattern = re.compile(r"Combine:\s*(.+)", re.IGNORECASE)
        combined_groups: List[List[str]] = []
        
        for line in notes_content.splitlines():
            match = combine_pattern.match(line.strip())
            if match:
                # Split by comma and strip whitespace
                combined_locations_names = [name.strip() for name in match.group(1).split(',')]
                combined_groups.append(combined_locations_names)
        
        # Keep track of locations that have been combined or processed
        processed_location_names = set()
        new_locations_list: List[Dict[str, Any]] = []

        for group in combined_groups:
            combined_name_parts = []
            combined_description_parts = []
            group_found_locations: List[Dict[str, Any]] = []

            for loc_name_to_combine in group:
                found_loc = next((loc for loc in current_locations if loc['name'] == loc_name_to_combine), None)
                if found_loc:
                    group_found_locations.append(found_loc)
                    combined_name_parts.append(loc_name_to_combine)
                    combined_description_parts.append(
                        f"### {loc_name_to_combine}\n{found_loc.get('description_text', '').strip()}"
                    )
                    processed_location_names.add(loc_name_to_combine)
                else:
                    print(f"Warning: Location '{loc_name_to_combine}' from grouping notes not found in extracted locations. Skipping this part of the combination.")
            
            if group_found_locations:
                # Create a new "meta-location"
                new_meta_location = {
                    'name': "_".join(combined_name_parts).replace(" ", "_"), # Create a consistent name
                    'description_text': "\n\n".join(combined_description_parts)
                }
                new_locations_list.append(new_meta_location)
        
        # Add any locations that were not part of a combined group
        for loc in current_locations:
            if loc['name'] not in processed_location_names:
                new_locations_list.append(loc)
        
        current_locations = new_locations_list

    processed_locations_data = {'locations': current_locations}
    processed_locations_path = work_dir / f"{adventure_name}.processed_locations.yaml"
    
    with open(processed_locations_path, "w", encoding="utf-8") as f:
        yaml.dump(processed_locations_data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)

    print(f"Processed locations saved to {processed_locations_path}")
    return processed_locations_path

def run(pdf_path: str, dry_run: bool = False):
    work_dir = Path("work")
    adventure_name = Path(pdf_path).stem
    
    # NEW: Apply manual grouping first
    try:
        locations_file_path = apply_manual_grouping(adventure_name)
    except FileNotFoundError as e:
        print(e)
        return

    # Load processed locations
    with open(locations_file_path, "r", encoding="utf-8") as f:
        locations_data = yaml.safe_load(f)
    
    if not locations_data or 'locations' not in locations_data:
        print(f"Error: No 'locations' key found in {locations_file_path}. Exiting.")
        return

    # Get the *full raw text* of the adventure for context during grouping
    from src.extract_locations import extract_text as get_raw_adventure_text
    full_raw_adventure_text = get_raw_adventure_text(pdf_path)

    # Prepare locations for the prompt (using processed locations)
    formatted_locations = []
    for loc in locations_data['locations']:
        formatted_locations.append(f"  - name: {loc['name']}\n    description_text: |\n      {textwrap.indent(loc['description_text'].strip(), '      ')}")
    locations_list_for_prompt = "\n".join(formatted_locations)

    # Load shared references and adventure outline/notes
    rules_reference = Path("data/rules_reference.md").read_text(encoding="utf-8")
    setting_reference = Path("data/setting_reference.md").read_text(encoding="utf-8")
    
    # Assume adventure outline exists from summarize_adventure.py
    adventure_outline_path = work_dir / f"{adventure_name}_summary_prompt.response.md"
    adventure_outline_md = ""
    if adventure_outline_path.exists():
        adventure_outline_md = adventure_outline_path.read_text(encoding="utf-8")
    else:
        print(f"Warning: Adventure outline not found at {adventure_outline_path}. Prompt may lack full context.")
        adventure_outline_md = "## Adventure Outline (Placeholder)\n\nNo outline provided."

    # Render Jinja2 template for scene grouping
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("group_scenes_prompt.md.j2")

    prompt = template.render(
        identified_locations=locations_list_for_prompt,
        full_adventure_text=textwrap.indent(full_raw_adventure_text.strip(), "    "),
        system_reference=rules_reference,
        setting_reference=setting_reference,
        adventure_outline=adventure_outline_md
    )

    llm_response_md = send_prompt_to_openrouter(prompt_md=prompt, prompt_name=prompt_path(pdf_path), dry_run=dry_run)

    if not dry_run and llm_response_md:
        extracted_scenes_data = extract_all_yaml_blocks_from_markdown(llm_response_md)

        if extracted_scenes_data:
            output_dir = output_scenes_dir(adventure_name)
            for i, scene_yaml_str in enumerate(extracted_scenes_data):
                try:
                    all_docs_in_block = list(yaml.safe_load_all(quote_colon_strings(scene_yaml_str)))
                    
                    if not all_docs_in_block:
                        print(f"Warning: No YAML documents found in block for scene {i+1} (block content might be empty or malformed). Skipping.")
                        continue
                    
                    scene_data = all_docs_in_block[0]
                    
                    if len(all_docs_in_block) > 1:
                        print(f"Warning: Multiple YAML documents found within a single markdown code block for scene {i+1}. Using only the first document.")
                    
                    scene_number = scene_data.get('scene_number', i + 1)
                    scene_title = scene_data.get('scene_title', f"Untitled Scene {scene_number}")
                    sanitized_title = re.sub(r'[^\w\-_\. ]', '', scene_title).replace(" ", "_").lower()
                    
                    scene_output_path = output_dir / f"scene_{scene_number:02d}_{sanitized_title}.yaml"
                    
                    with open(scene_output_path, "w", encoding="utf-8") as f:
                        f.write(scene_yaml_str)
                    print(f"Saved grouped scene {scene_number} to {scene_output_path}")
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML for scene {i+1}: {e}\nRaw YAML:\n{scene_yaml_str}")
                except Exception as e:
                    print(f"An unexpected error occurred for scene {i+1}: {e}\nRaw YAML:\n{scene_yaml_str}")
        else:
            print("No YAML scenes found in LLM response.")