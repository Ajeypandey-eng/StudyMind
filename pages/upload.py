import streamlit as st
import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    text = ""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        st.error(f"Failed to read PDF **{file.name}**: {e}")
    return text

def upload_page():
    st.markdown("""
    <div style="padding:10px 0 24px;">
      <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#475569;
                  letter-spacing:.15em;margin-bottom:8px;">KNOWLEDGE BASE</div>
      <h1>Upload Study Documents</h1>
      <p style="color:#64748b;font-size:0.9rem;margin-top:4px;">
        Upload your PDFs and TXT notes. The AI reads <strong style="color:#c084fc;">only these files</strong> — no external knowledge or API key used.
      </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">UPLOAD FILES</div>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Drop PDFs or TXT files here",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("⚡  Process Documents", type="primary", use_container_width=True):
            if not uploaded_files:
                st.warning("Please upload at least one file first.")
            else:
                added_count = 0
                with st.spinner("Extracting text from documents..."):
                    for file in uploaded_files:
                        if file.name not in st.session_state.documents:
                            if file.name.lower().endswith(".pdf"):
                                text = extract_text_from_pdf(file)
                            else:
                                try:
                                    text = file.read().decode("utf-8")
                                except Exception as e:
                                    st.error(f"Failed to read **{file.name}**: {e}")
                                    text = ""
                            if text.strip():
                                st.session_state.documents[file.name] = text
                                added_count += 1

                if added_count > 0:
                    st.success(f"✅ Successfully indexed **{added_count}** new document(s)!")
                else:
                    st.info("All files are already in the library, or no text could be extracted.")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#0f1117;border:1px solid #1e2235;border-radius:10px;padding:16px 18px;">
          <div style="font-size:0.75rem;font-weight:600;color:#67e8f9;margin-bottom:10px;">💡 Tips for best results</div>
          <ul style="color:#475569;font-size:0.8rem;line-height:1.9;margin:0;padding-left:16px;">
            <li>Use text-based PDFs (not scanned images)</li>
            <li>Upload chapter-by-chapter for precise retrieval</li>
            <li>TXT files with clear headings work great</li>
            <li>Larger context = more accurate Q&A answers</li>
          </ul>
        </div>""", unsafe_allow_html=True)

    with right:
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">DOCUMENT LIBRARY</div>', unsafe_allow_html=True)

        if not st.session_state.documents:
            st.markdown("""
            <div style="background:#0f1117;border:1px dashed #1e2235;border-radius:10px;
                        padding:32px;text-align:center;">
              <div style="font-size:2rem;margin-bottom:8px;opacity:.4;">📚</div>
              <div style="color:#334155;font-size:0.82rem;">No documents yet.<br/>Upload files to get started.</div>
            </div>""", unsafe_allow_html=True)
        else:
            total_chars = sum(len(v) for v in st.session_state.documents.values())
            st.markdown(f"""
            <div style="display:flex;gap:10px;margin-bottom:14px;">
              <div style="flex:1;background:#13151f;border:1px solid #1e2235;border-radius:8px;padding:12px;text-align:center;">
                <div style="font-size:1.4rem;font-weight:700;color:#c084fc;">{len(st.session_state.documents)}</div>
                <div style="font-size:0.7rem;color:#475569;">Documents</div>
              </div>
              <div style="flex:1;background:#13151f;border:1px solid #1e2235;border-radius:8px;padding:12px;text-align:center;">
                <div style="font-size:1.4rem;font-weight:700;color:#67e8f9;">{total_chars//1000}K</div>
                <div style="font-size:0.7rem;color:#475569;">Characters</div>
              </div>
            </div>""", unsafe_allow_html=True)

            for doc_name in st.session_state.documents:
                chars = len(st.session_state.documents[doc_name])
                is_pdf = doc_name.lower().endswith(".pdf")
                icon = "📕" if is_pdf else "📝"
                short = doc_name if len(doc_name) <= 30 else doc_name[:27] + "..."
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:11px 14px;
                            background:#0f1117;border:1px solid #1e2235;border-radius:8px;margin-bottom:6px;">
                  <span style="font-size:18px;">{icon}</span>
                  <div style="flex:1;min-width:0;">
                    <div style="font-size:0.82rem;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{short}</div>
                    <div style="font-size:0.65rem;color:#334155;font-family:'JetBrains Mono',monospace;">
                      {'PDF' if is_pdf else 'TXT'} · {chars:,} chars
                    </div>
                  </div>
                  <div style="width:6px;height:6px;background:#86efac;border-radius:50%;box-shadow:0 0 5px #86efac80;flex-shrink:0;"></div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🗑  Clear All Documents", type="secondary", use_container_width=True):
                st.session_state.documents = {}
                st.success("Library cleared.")
                st.rerun()
