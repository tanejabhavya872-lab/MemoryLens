# MemoryLens

An AI-powered local memory assistant that captures your screen, extracts text via OCR, and enables natural-language semantic search over your screenshot history using CLIP embeddings and FAISS — all running entirely on your own machine.

## What it does

MemoryLens periodically captures screenshots of your screen, reads any visible text using OCR, and generates a semantic "visual fingerprint" (embedding) of each image using OpenAI's CLIP model. All of this is stored locally in a SQLite database. A Streamlit interface then lets you search your screen history using plain English — like *"find the screenshot of a code editor"* — and instantly see the most relevant matches, powered by a FAISS vector similarity search.

No cloud services, no external APIs for the core pipeline, no data leaves your machine.

## Features

- 🖥️ **Automatic screen capture** — timestamped screenshots saved locally
- 📝 **OCR text extraction** — reads on-screen text using EasyOCR
- 🧠 **CLIP-based image embeddings** — understands the visual meaning of each screenshot, not just its text
- 🔍 **Semantic search** — search using natural language, not just exact keywords
- ⚡ **FAISS vector search** — instant similarity search, even across large screenshot collections
- 💾 **Local SQLite database** — all metadata, OCR text, and embeddings stored locally
- 🔁 **Smart screen-change detection** — skips saving near-duplicate screenshots when the screen hasn't meaningfully changed, reducing storage use and redundant processing
- 🌐 **Streamlit UI** — simple, interactive search interface in your browser

## Architecture
## Tech Stack

| Component | Technology |
|---|---|
| Screen capture | `mss` |
| OCR | `EasyOCR` |
| Computer vision / embeddings | `PyTorch`, `OpenAI CLIP (ViT-B/32)` |
| Vector search | `FAISS` |
| Database | `SQLite` |
| UI | `Streamlit` |

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Installation

```bash
git clone https://github.com/tanejabhavya872-lab/MemoryLens.git
cd MemoryLens
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

### Usage

1. **Capture screenshots:**
```bash
   python src\capture\screenshot.py
```
   (Runs continuously, capturing every 5 seconds — stop with `Ctrl+C`)

2. **Set up the database:**
```bash
   python src\db\database.py
   python src\db\add_embedding_column.py
```

3. **Extract text from screenshots (OCR):**
```bash
   python src\ocr\extract_text.py
```

4. **Generate CLIP embeddings:**
```bash
   python src\vision\generate_embeddings.py
```

5. **Launch the search app:**
```bash
   streamlit run src\ui\app.py
```

Or simply double-click `run_app.bat` to launch the app directly.

## Project Structure
## Roadmap

### Completed
- [x] Project setup, folder structure, Git/GitHub
- [x] Screen capture (mss)
- [x] Screen-change detection (skip duplicate captures)
- [x] OCR text extraction (EasyOCR)
- [x] SQLite database (screenshots, OCR text, embeddings)
- [x] CLIP embeddings (image + text)
- [x] FAISS vector similarity search
- [x] Streamlit UI
- [x] Hybrid search (keyword + semantic scoring)
- [x] FastAPI backend (API/UI separation)
- [x] Launcher scripts (`run_app.bat`, optional `start_capture.bat`)

### Planned
- [ ] Re-run OCR + embeddings on newly captured screenshots
- [ ] Duplicate/near-duplicate cleanup for older screenshots
- [ ] Date/time filtering and a "browse by date" view
- [ ] Retention policy (auto-delete screenshots older than X days)
- [ ] Simple pause/resume control for capture
- [ ] Additional API endpoints (e.g. fetch single screenshot metadata)
## Optional: Auto-start capture on login
`start_capture.bat` can be used to run the screen capture script in the background.
To have it start automatically when you log in to Windows, you can register it as a
scheduled task via Task Scheduler (Trigger: "At log on", Action: run `start_capture.bat`,
check "Hidden" to suppress the console window). This is optional — capture also works
fine when started manually.
## Privacy Note

This tool captures screenshots of your own screen, which may include sensitive personal information. All data is stored **locally only** — screenshots, extracted text, and the database are excluded from version control via `.gitignore` and are never uploaded anywhere.

## Author

**Bhavya Taneja**