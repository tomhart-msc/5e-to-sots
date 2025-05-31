def load_notes_md(path):
    tone = None
    intent = ""
    allow_invention = False
    current_section = None
    sections = {"tone": "", "notes": "", "obstacles": "", "allow invention": ""}

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith("## "):
                current_section = line[3:].strip().lower()
            elif current_section:
                sections[current_section] += line + "\n"

    tone = sections["tone"].strip()
    notes = sections["notes"].strip()
    obstacles = sections["obstacles"].strip()
    allow_invention = "yes" in sections["allow invention"].lower()

    return {
        "tone": tone or None,
        "notes": notes or "",
        "obstacles": obstacles or None,
        "allow_invention": allow_invention
    }