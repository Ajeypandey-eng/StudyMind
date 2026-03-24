import streamlit as st

def home_page():
    st.markdown("""
    <div style="padding: 10px 0 28px;">
      <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#475569;
                  letter-spacing:.15em;margin-bottom:10px;">LOCAL AI · STUDY · PLATFORM</div>
      <h1 style="font-size:2.4rem!important;margin-bottom:10px;">
        Your Second Brain,<br/>Runs Locally
      </h1>
      <p style="color:#64748b;font-size:1rem;max-width:540px;line-height:1.7;margin-bottom:0;">
        StudyMind is a fully local RAG-based study assistant. It reads your notes, answers questions,
        generates flashcards, and builds study schedules — powered by HuggingFace models on your machine.
        <strong style="color:#86efac;">No API key. No internet. No data leaves your device.</strong>
      </p>
    </div>
    """, unsafe_allow_html=True)

    doc_count   = len(st.session_state.documents)
    fc_count    = len(st.session_state.current_flashcards)
    sched_count = len(st.session_state.current_schedule)
    chat_count  = len([m for m in st.session_state.chat_history if m["role"] == "user"])

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, icon in [
        (c1, doc_count,   "Documents",     "📄"),
        (c2, fc_count,    "Flashcards",    "🃏"),
        (c3, sched_count, "Schedule Days", "📅"),
        (c4, chat_count,  "Q&A Exchanges", "💬"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#13151f;border:1px solid #1e2235;border-radius:12px;
                        padding:18px 20px;position:relative;overflow:hidden;">
              <div style="position:absolute;top:-10px;right:10px;font-size:3rem;opacity:.08;">{icon}</div>
              <div style="font-size:2rem;font-weight:800;color:#c084fc;font-family:'Outfit',sans-serif;">{val}</div>
              <div style="font-size:0.78rem;color:#475569;margin-top:2px;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # Model info banner
    st.markdown("""
    <div style="background:linear-gradient(135deg,#052e16,#0c1a2e);border:1px solid #166534;
                border-radius:12px;padding:14px 20px;margin-bottom:24px;display:flex;align-items:center;gap:14px;">
      <div style="font-size:1.4rem;">🟢</div>
      <div>
        <div style="font-size:0.8rem;font-weight:600;color:#86efac;margin-bottom:2px;">Running 100% locally — No API key required</div>
        <div style="font-size:0.72rem;color:#475569;font-family:'JetBrains Mono',monospace;">
          Embeddings: all-MiniLM-L6-v2 (HuggingFace) &nbsp;·&nbsp; Generator: google/flan-t5-base (HuggingFace)
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:14px;">FEATURES</div>', unsafe_allow_html=True)

    features = [
        ("📄", "Upload Docs",   "upload",     "#7c3aed",
         "Upload PDFs and TXT notes. Text is extracted locally with PyMuPDF — no cloud storage."),
        ("💬", "RAG Q&A",       "qa",          "#0e7490",
         "Ask questions. Answers are semantically retrieved and generated entirely on-device."),
        ("🃏", "Flashcards",    "flashcards",  "#7c3aed",
         "Auto-generate Q&A flashcard decks using flan-t5 from your study material."),
        ("📅", "Study Planner", "planner",     "#0e7490",
         "Get a smart Pomodoro schedule tailored to your subjects and exam date — no LLM call needed."),
    ]

    col_pairs = [st.columns(2), st.columns(2)]
    for i, (icon, title, page_id, color, desc) in enumerate(features):
        row, col_idx = divmod(i, 2)
        with col_pairs[row][col_idx]:
            st.markdown(f"""
            <div style="background:#13151f;border:1px solid #1e2235;border-radius:12px;
                        padding:20px;margin-bottom:12px;border-left:3px solid {color};">
              <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
              <div style="font-weight:700;font-size:0.95rem;color:#e2e8f0;margin-bottom:6px;">{title}</div>
              <div style="font-size:0.82rem;color:#64748b;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"home_btn_{page_id}"):
                st.session_state.page = page_id
                st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#13151f,#0f1117);border:1px solid #2d2f45;
                border-radius:14px;padding:24px 28px;">
      <div style="font-weight:700;color:#c084fc;font-size:0.95rem;margin-bottom:14px;">⚡ Quick Start Guide</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;">
        <div style="text-align:center;">
          <div style="width:32px;height:32px;background:#1e1535;border:1px solid #7c3aed50;
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:14px;margin:0 auto 8px;">1</div>
          <div style="font-size:0.78rem;color:#64748b;">Upload your<br/>PDF/TXT notes</div>
        </div>
        <div style="text-align:center;">
          <div style="width:32px;height:32px;background:#0c1a2e;border:1px solid #0e749050;
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:14px;margin:0 auto 8px;">2</div>
          <div style="font-size:0.78rem;color:#64748b;">Ask questions<br/>in RAG Q&A</div>
        </div>
        <div style="text-align:center;">
          <div style="width:32px;height:32px;background:#1e1535;border:1px solid #7c3aed50;
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:14px;margin:0 auto 8px;">3</div>
          <div style="font-size:0.78rem;color:#64748b;">Generate<br/>flashcards</div>
        </div>
        <div style="text-align:center;">
          <div style="width:32px;height:32px;background:#0c1a2e;border:1px solid #0e749050;
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:14px;margin:0 auto 8px;">4</div>
          <div style="font-size:0.78rem;color:#64748b;">Build a study<br/>schedule</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
