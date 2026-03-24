"""
local_ai.py  –  StudyMind's fully local AI engine
Uses:
  • sentence-transformers  → embeddings + semantic search
  • transformers (flan-t5) → text generation (QA, flashcards, planner)
No external API keys required.
"""

import numpy as np
import json
import re
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity


# ── Model loading (cached so it only loads once per session) ──────────────────

@st.cache_resource(show_spinner=False)
def load_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")   # ~90 MB, fast CPU inference


@st.cache_resource(show_spinner=False)
def load_generator():
    from transformers import pipeline
    # flan-t5-base: instruction-tuned, ~250 MB, runs well on CPU
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=512,
        do_sample=False,
    )


# ── Embedding helpers ─────────────────────────────────────────────────────────

def embed_texts(texts: list[str]) -> np.ndarray:
    embedder = load_embedder()
    return embedder.encode(texts, convert_to_numpy=True, show_progress_bar=False)


def embed_query(query: str) -> np.ndarray:
    embedder = load_embedder()
    return embedder.encode([query], convert_to_numpy=True, show_progress_bar=False)


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks


# ── RAG retrieval ─────────────────────────────────────────────────────────────

def get_top_chunks(query: str, documents: dict, top_n: int = 4) -> list[dict]:
    """
    Semantic search over all document chunks.
    Returns top_n chunks sorted by cosine similarity to the query.
    """
    all_chunks = []
    for doc_name, text in documents.items():
        for chunk in chunk_text(text):
            all_chunks.append({"doc_name": doc_name, "text": chunk})

    if not all_chunks:
        return []

    chunk_texts = [c["text"] for c in all_chunks]
    chunk_embs  = embed_texts(chunk_texts)          # (N, 384)
    query_emb   = embed_query(query)                # (1, 384)

    scores = cosine_similarity(query_emb, chunk_embs)[0]  # (N,)
    top_indices = np.argsort(scores)[::-1][:top_n]

    return [
        {**all_chunks[i], "score": float(scores[i])}
        for i in top_indices
        if scores[i] > 0.1           # drop near-zero matches
    ]


# ── Answer generation ─────────────────────────────────────────────────────────

def answer_question(query: str, documents: dict) -> tuple[str, list[dict]]:
    """
    RAG pipeline:  retrieve → build prompt → generate answer
    Returns (answer_text, top_chunks_used)
    """
    top_chunks = get_top_chunks(query, documents)

    if not top_chunks:
        return "I couldn't find relevant information in your uploaded documents.", []

    context = "\n\n".join(
        [f"[From: {c['doc_name']}]\n{c['text']}" for c in top_chunks]
    )

    prompt = (
        f"You are a helpful study tutor. Answer the question based ONLY on the context below. "
        f"If the answer is not in the context, say 'Not found in documents'. "
        f"Be concise and clear.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )

    generator = load_generator()
    result = generator(prompt)[0]["generated_text"].strip()

    # Prepend source citations
    sources = list({c["doc_name"] for c in top_chunks})
    citation = f"*Sources: {', '.join(sources)}*\n\n"
    return citation + result, top_chunks


# ── Flashcard generation ──────────────────────────────────────────────────────

# Different question stems to force variety across cards
_Q_STEMS = [
    "What is the definition of",
    "Explain the concept of",
    "What are the key steps involved in",
    "How does {} work in the context of",
    "What is the difference between {} and related concepts in",
    "Give an example of",
    "What are the main characteristics of",
    "Why is {} important in",
    "Describe the process of",
    "What problem does {} solve in",
]


def _get_diverse_chunks(topic: str, documents: dict, num_cards: int) -> list[str]:
    """
    Returns a list of num_cards context strings, each from a DIFFERENT chunk,
    so every flashcard has a unique piece of source material.
    """
    all_chunks = []
    for doc_name, text in documents.items():
        for chunk in chunk_text(text, chunk_size=500, overlap=50):
            all_chunks.append(chunk)

    if not all_chunks:
        return [""] * num_cards

    # Embed all chunks + topic query, rank by similarity
    chunk_embs = embed_texts(all_chunks)
    query_emb  = embed_query(topic)
    scores     = cosine_similarity(query_emb, chunk_embs)[0]
    ranked_idx = np.argsort(scores)[::-1]

    # Take top-N distinct chunks (one per card)
    selected = []
    for idx in ranked_idx:
        selected.append(all_chunks[idx])
        if len(selected) >= num_cards:
            break

    # Pad with earlier chunks if not enough
    while len(selected) < num_cards:
        selected.append(all_chunks[len(selected) % len(all_chunks)])

    return selected


def generate_flashcards(topic: str, documents: dict, num_cards: int = 6) -> list[dict]:
    """
    Generates Q&A flashcards on a topic using document context.
    Each card uses a DIFFERENT source chunk and a DIFFERENT question stem.
    Returns list of {"question": ..., "answer": ...}
    """
    generator = load_generator()

    # Get one unique chunk per card
    per_card_chunks = _get_diverse_chunks(topic, documents, num_cards)

    cards = []
    seen_questions = set()

    for i in range(num_cards):
        chunk = per_card_chunks[i]
        # Pick a different question stem for each card (cycle through list)
        stem = _Q_STEMS[i % len(_Q_STEMS)]
        # Fill placeholder if stem uses .format()
        if "{}" in stem:
            stem = stem.replace("{}", topic)

        # Build a tightly focused question prompt using THIS chunk only
        q_prompt = (
            f"Read the following study material excerpt carefully.\n"
            f"Material: {chunk[:600]}\n\n"
            f"Write a specific exam question starting with: '{stem}'\n"
            f"The question must be answerable from the material above.\n"
            f"Question:"
        )

        # Build answer prompt: question + same chunk
        try:
            question = generator(q_prompt, max_new_tokens=80)[0]["generated_text"].strip()

            # Deduplicate — if same question generated, tweak the stem
            if question in seen_questions or len(question) < 10:
                question = f"{stem} {topic} as described in your notes?"

            seen_questions.add(question)

            a_prompt = (
                f"Material: {chunk[:600]}\n\n"
                f"Question: {question}\n\n"
                f"Give a concise, accurate answer based only on the material above.\n"
                f"Answer:"
            )
            answer = generator(a_prompt, max_new_tokens=120)[0]["generated_text"].strip()

            if not answer or len(answer) < 5:
                answer = "Refer to this section of your study material for details."

            cards.append({"question": question, "answer": answer})

        except Exception as e:
            cards.append({
                "question": f"{stem} {topic}?",
                "answer": f"See your uploaded notes on {topic}.",
            })

    return cards if cards else [{"question": f"Define {topic}.", "answer": "See your study notes."}]


# ── Study planner generation ──────────────────────────────────────────────────

def generate_schedule(subjects: str, exam_date: str, hours_per_day: int) -> list[dict]:
    """
    Generates a day-by-day study schedule.
    Returns list of schedule session dicts.
    Cross-platform safe — no %-d or platform-specific strftime codes.
    """
    from datetime import datetime, timedelta

    # ── Parse exam date — accept multiple common formats ──────────────────
    exam_dt = None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d %b %Y", "%d %B %Y"):
        try:
            exam_dt = datetime.strptime(exam_date.strip(), fmt)
            break
        except ValueError:
            continue

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    if exam_dt is None:
        # Could not parse — use 14-day default and warn via return value
        days_left = 14
    else:
        days_left = (exam_dt - today).days

    days_left = max(1, min(days_left, 60))  # cap at 60 days

    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
    if not subject_list:
        subject_list = [subjects.strip()]

    phase_labels = {
        "Study":    "Core Concepts",
        "Review":   "Revision & Notes",
        "Practice": "Problems & MCQs",
    }
    cycle = ["Study", "Review", "Practice"]

    schedule = []
    for day_num in range(days_left):
        date = today + timedelta(days=day_num)

        # Cross-platform date string: "Mon Apr 7" — use date.day (int, no leading zero)
        day_label = f"Day {day_num + 1} - {date.strftime('%a %b')} {date.day}"

        # Rest every 4th day
        if (day_num + 1) % 4 == 0:
            stype       = "Rest"
            session_topic = "Rest & Consolidation"
            hrs         = max(1, hours_per_day // 2)
        else:
            subject    = subject_list[day_num % len(subject_list)]
            stype      = cycle[day_num % 3]
            session_topic = f"{subject} - {phase_labels[stype]}"   # ASCII dash, not en-dash
            hrs        = hours_per_day

        schedule.append({
            "day":            day_label,
            "topic":          session_topic,
            "session_type":   stype,
            "hours":          hrs,
            "pomodoro_count": hrs * 2,
        })

    return schedule
