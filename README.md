# StudyMind AI — Local Edition 🧠

**Fully local RAG study assistant. No API key. No internet. No data leaves your device.**

## Models Used (HuggingFace, downloaded on first run)
| Model | Purpose | Size |
|-------|---------|------|
| `sentence-transformers/all-MiniLM-L6-v2` | Embeddings + Semantic Search | ~90 MB |
| `google/flan-t5-base` | Q&A + Flashcard Generation | ~250 MB |

Models are cached by HuggingFace after first download (~340 MB total).

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

On first launch, models download automatically (~30–60s depending on internet speed).
After that, everything runs **fully offline**.

---

## Project Structure

```
StudyMind-Local/
├── app.py                    # Entry point
├── local_ai.py               # All AI logic (embeddings, RAG, generation)
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── components/
│   └── sidebar.py
└── pages/
    ├── home.py
    ├── upload.py
    ├── qa.py
    ├── flashcards.py
    └── planner.py
```

## How It Works

### RAG Pipeline (Q&A)
1. Your documents are chunked into 400-char segments with 80-char overlap
2. Query is embedded with `all-MiniLM-L6-v2` into a 384-dim vector
3. Cosine similarity search finds the top-4 most relevant chunks
4. Chunks + question are passed to `flan-t5-base` for answer generation

### Flashcards
- Topic is semantically searched against your documents
- `flan-t5-base` generates question + answer pairs from retrieved context

### Study Planner
- Fully deterministic — no LLM call needed
- Rotates subjects across Study → Review → Practice cycles
- Inserts Rest days every 4th day
- Calculates Pomodoro count (2 per hour)

---

## Performance Notes
- **CPU inference**: flan-t5-base runs ~3–5s per generation on modern CPU
- **GPU**: If you have CUDA, install `torch` with GPU support for faster inference
- **Memory**: ~600 MB RAM for both models loaded simultaneously
