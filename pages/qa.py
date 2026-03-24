import streamlit as st
from local_ai import answer_question

def qa_page():
    st.markdown("""
    <div style="padding:10px 0 20px;">
      <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#475569;
                  letter-spacing:.15em;margin-bottom:8px;">RAG PIPELINE</div>
      <h1>AI Tutor Chat</h1>
      <p style="color:#64748b;font-size:0.88rem;margin-top:4px;">
        Answers are grounded <strong style="color:#c084fc;">strictly in your documents</strong>.
        Powered by local HuggingFace models — no API key needed.
      </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.documents:
        st.markdown("""
        <div style="background:#0f1117;border:1px dashed #2d2f45;border-radius:12px;
                    padding:40px;text-align:center;margin-top:20px;">
          <div style="font-size:2.5rem;margin-bottom:12px;">📄</div>
          <div style="font-size:1rem;color:#475569;margin-bottom:16px;">No documents uploaded yet.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("→ Upload Documents", type="primary"):
            st.session_state.page = "upload"
            st.rerun()
        return

    chat_col, info_col = st.columns([3, 1], gap="large")

    with chat_col:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        query = st.chat_input("Ask anything about your uploaded documents...")

        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                with st.spinner("Searching documents & generating answer..."):
                    answer, chunks = answer_question(query, st.session_state.documents)

                st.markdown(answer)

                # Show retrieved chunks as sources
                if chunks:
                    with st.expander("📎 Retrieved context chunks"):
                        for c in chunks:
                            score_pct = int(c.get("score", 0) * 100)
                            st.markdown(f"""
                            <div style="background:#0f1117;border:1px solid #1e2235;border-radius:8px;
                                        padding:10px 14px;margin-bottom:8px;">
                              <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                                <span style="font-size:0.72rem;color:#67e8f9;font-family:'JetBrains Mono',monospace;">{c['doc_name']}</span>
                                <span style="font-size:0.68rem;color:#334155;font-family:'JetBrains Mono',monospace;">similarity: {score_pct}%</span>
                              </div>
                              <div style="font-size:0.78rem;color:#64748b;line-height:1.6;">{c['text'][:300]}...</div>
                            </div>""", unsafe_allow_html=True)

                st.session_state.chat_history.append({"role": "assistant", "content": answer})

    with info_col:
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">SOURCES ACTIVE</div>', unsafe_allow_html=True)

        for doc_name in st.session_state.documents:
            short = doc_name if len(doc_name) <= 22 else doc_name[:19] + "..."
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                        background:#0f1117;border:1px solid #1e2235;border-radius:7px;margin-bottom:5px;">
              <div style="width:6px;height:6px;background:#86efac;border-radius:50%;box-shadow:0 0 5px #86efac80;flex-shrink:0;"></div>
              <div style="font-size:0.75rem;color:#64748b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{short}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        if st.session_state.chat_history:
            if st.button("🗑 Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("""
        <div style="background:#0f1117;border:1px solid #1e2235;border-radius:10px;padding:14px 16px;margin-top:8px;">
          <div style="font-size:0.72rem;font-weight:600;color:#67e8f9;margin-bottom:10px;">⚙️ How it works (local)</div>
          <div style="font-size:0.72rem;color:#475569;line-height:1.9;">
            1. Query embedded with <span style="color:#c084fc;">MiniLM-L6</span><br/>
            2. Cosine similarity search over chunks<br/>
            3. Top chunks sent to <span style="color:#c084fc;">flan-t5-base</span><br/>
            4. Answer generated — no internet needed
          </div>
        </div>""", unsafe_allow_html=True)
