import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:22px 20px 10px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#7c3aed,#0e7490);
                        border-radius:8px;display:flex;align-items:center;justify-content:center;
                        font-size:17px;box-shadow:0 0 14px #7c3aed50;">🧠</div>
            <div>
              <div style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.05rem;
                          background:linear-gradient(135deg,#c084fc,#67e8f9);
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                StudyMind
              </div>
              <div style="font-size:0.65rem;color:#475569;font-family:'JetBrains Mono',monospace;
                          margin-top:-2px;">LOCAL AI · NO API KEY</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="padding:0 14px 8px;">', unsafe_allow_html=True)
        if st.button("⬆  Upload Notes", use_container_width=True, key="sb_upload"):
            st.session_state.page = "upload"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr style="margin:4px 0 10px;border-color:#1e2235;">', unsafe_allow_html=True)

        st.markdown('<div style="padding:0 14px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:8px;">NAVIGATION</div>', unsafe_allow_html=True)

        nav_items = [
            ("home",       "🏠", "Home"),
            ("upload",     "📄", "Upload Docs"),
            ("qa",         "💬", "RAG Q&A Chat"),
            ("flashcards", "🃏", "Flashcards"),
            ("planner",    "📅", "Study Planner"),
        ]
        for page_id, icon, label in nav_items:
            if st.button(f"{icon}  {label}", use_container_width=True, key=f"nav_{page_id}"):
                st.session_state.page = page_id
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<hr style="margin:10px 0;border-color:#1e2235;">', unsafe_allow_html=True)

        # Library
        st.markdown('<div style="padding:0 14px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:8px;">LIBRARY</div>', unsafe_allow_html=True)

        if st.session_state.documents:
            for doc_name in st.session_state.documents:
                short = doc_name if len(doc_name) <= 26 else doc_name[:23] + "..."
                chars = len(st.session_state.documents[doc_name])
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:7px 10px;
                            background:#0f1117;border:1px solid #1e2235;border-radius:7px;margin-bottom:5px;">
                  <span style="font-size:14px;">📝</span>
                  <div style="flex:1;min-width:0;">
                    <div style="font-size:0.78rem;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{short}</div>
                    <div style="font-size:0.62rem;color:#334155;font-family:'JetBrains Mono',monospace;">{chars:,} chars</div>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:0.78rem;color:#334155;padding:6px 0;font-style:italic;">No documents yet</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<hr style="margin:10px 0;border-color:#1e2235;">', unsafe_allow_html=True)

        # Today's plan
        st.markdown('<div style="padding:0 14px 16px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:8px;">TODAY\'S PLAN</div>', unsafe_allow_html=True)

        if st.session_state.current_schedule:
            for i, task in enumerate(st.session_state.current_schedule[:3]):
                label = task.get('topic', f'Session {i+1}')[:28]
                stype = task.get('session_type', 'Study')
                hrs   = task.get('hours', 0)
                color = {"Study":"#c084fc","Review":"#67e8f9","Practice":"#86efac","Rest":"#94a3b8"}.get(stype, "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:7px 10px;
                            background:#0f1117;border:1px solid #1e2235;border-radius:7px;margin-bottom:5px;">
                  <div style="width:7px;height:7px;border-radius:50%;background:{color};flex-shrink:0;box-shadow:0 0 6px {color}80;"></div>
                  <div style="flex:1;min-width:0;">
                    <div style="font-size:0.75rem;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{label}</div>
                    <div style="font-size:0.62rem;color:#334155;font-family:'JetBrains Mono',monospace;">{stype} · {hrs}h</div>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#0f1117;border:1px solid #1e2235;border-radius:7px;padding:12px;text-align:center;">
              <div style="font-size:18px;margin-bottom:4px;">📅</div>
              <div style="font-size:0.72rem;color:#334155;">No schedule yet.<br/>Use Study Planner!</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Model status badge
        st.markdown("""
        <div style="position:absolute;bottom:16px;left:0;right:0;padding:0 20px;">
          <div style="background:#0f1117;border:1px solid #1e2235;border-radius:6px;padding:6px 10px;text-align:center;">
            <div style="font-size:0.6rem;color:#334155;font-family:'JetBrains Mono',monospace;">
              🟢 Running fully locally
            </div>
            <div style="font-size:0.58rem;color:#1e293b;font-family:'JetBrains Mono',monospace;margin-top:1px;">
              all-MiniLM-L6-v2 · flan-t5-base
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
