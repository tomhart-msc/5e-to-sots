# 5e-to-sots
Python scripts for orchestrating LLMs to convert 5e adventures to Swords of the Serpentine

## Setup

This repo uses `asdf`. Install Python with:

```
asdf plugin-add python
asdf install
```

Then install dependencies with:

```
pip install -r requirements.txt
```

## PDF Output

**Pandoc** is a powerful command-line tool for converting documents between different formats — for example, from Markdown (`.md`) to PDF, HTML, Word (`.docx`), LaTeX, and more. It's ideal for generating polished PDFs from text-based outputs like your converted adventure scenes.

---

### ✅ What You Can Do With Pandoc

In your case, you’d use it to:

* Combine multiple Markdown files into one.
* Convert that Markdown into a printable, shareable PDF.

---

### 📦 How to Install Pandoc

#### **macOS (using Homebrew)**

```bash
brew install pandoc
brew install weasyprint
```

#### **Ubuntu/Debian**

```bash
sudo apt update
sudo apt install pandoc
```

#### **Windows**

1. Go to [https://pandoc.org/installing.html](https://pandoc.org/installing.html)
2. Download the Windows installer.
3. Run the installer (it will also install optional GUI tools if you want them).

---

### 🖨️ Optional: Enable PDF output with LaTeX

To generate PDFs from Markdown, **Pandoc uses LaTeX under the hood**. You’ll want to install a LaTeX engine like **TeX Live** or **MacTeX**:

#### macOS

```bash
brew install --cask mactex-no-gui
```

#### Ubuntu/Debian

```bash
sudo apt install texlive-full
```

#### Windows

Install [MiKTeX](https://miktex.org/) or [TeX Live for Windows](https://www.tug.org/texlive/windows.html)

---

### 🧪 Test Pandoc

Once installed:

```bash
pandoc -v
```

And to convert Markdown to PDF:

```bash
pandoc myfile.md -o myfile.pdf
```

Let me know if you want a styled PDF (e.g., custom fonts or layout) — Pandoc is very customizable.
