import streamlit as st
from local_ai import generate_flashcards

def flashcards_page():
    st.markdown("""
    <div style="padding:10px 0 20px;">
      <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#475569;
                  letter-spacing:.15em;margin-bottom:8px;">ACTIVE RECALL</div>
      <h1>Flashcard Generator</h1>
      <p style="color:#64748b;font-size:0.88rem;margin-top:4px;">
        AI-generated flashcard decks from your notes — runs entirely on local HuggingFace models.
      </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.documents:
        st.markdown("""<div style="text-align:center;padding:40px;">
          <div style="font-size:2rem;margin-bottom:10px;">📄</div>
          <div style="color:#475569;">Upload documents first to generate flashcards.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("→ Upload Documents", type="primary"):
            st.session_state.page = "upload"
            st.rerun()
        return

    gen_col, view_col = st.columns([2, 3], gap="large")

    with gen_col:
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">GENERATE DECK</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:#0f1117;border:1px solid #1e2235;border-radius:12px;padding:20px;">', unsafe_allow_html=True)

        topic = st.text_input("Topic / Subject", placeholder="e.g., Automata Theory, KMP Algorithm...")
        num_cards = st.number_input("Number of Cards", min_value=1, max_value=10, value=5)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        st.info("💡 Local generation with flan-t5-base. Each card takes ~3–5 seconds on CPU.")

        if st.button("🃏  Generate Flashcards", type="primary", use_container_width=True):
            if not topic:
                st.warning("Enter a topic first.")
            else:
                with st.spinner(f"Generating {num_cards} flashcards locally... (this may take ~{num_cards * 5}s)"):
                    try:
                        cards = generate_flashcards(topic, st.session_state.documents, num_cards)
                        st.session_state.current_flashcards = cards
                        st.session_state.fc_index = 0
                        st.session_state.fc_revealed = False
                        st.success(f"✅ Generated {len(cards)} flashcards!")
                    except Exception as e:
                        st.error(f"Error during generation: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.current_flashcards:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">ALL CARDS</div>', unsafe_allow_html=True)

            for i, card in enumerate(st.session_state.current_flashcards):
                is_current = i == st.session_state.fc_index
                border = "#7c3aed" if is_current else "#1e2235"
                q_short = card.get("question","")[:60] + ("..." if len(card.get("question","")) > 60 else "")
                st.markdown(f"""
                <div style="padding:9px 12px;background:#0f1117;border:1px solid {border};
                            border-radius:7px;margin-bottom:5px;">
                  <div style="font-size:0.72rem;color:{'#c084fc' if is_current else '#64748b'};
                              font-weight:{'600' if is_current else '400'};">
                    {'▶ ' if is_current else ''}{i+1}. {q_short}
                  </div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Jump to card {i+1}", key=f"fc_jump_{i}", help=q_short):
                    st.session_state.fc_index = i
                    st.session_state.fc_revealed = False
                    st.rerun()

    with view_col:
        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">FOCUS AREA</div>', unsafe_allow_html=True)

        if not st.session_state.current_flashcards:
            st.markdown("""
            <div style="background:#0f1117;border:2px dashed #1e2235;border-radius:14px;
                        padding:60px 32px;text-align:center;">
              <div style="font-size:3rem;margin-bottom:12px;opacity:.3;">🃏</div>
              <div style="color:#334155;font-size:0.9rem;">Generate a flashcard deck to start studying.</div>
            </div>""", unsafe_allow_html=True)
        else:
            cards = st.session_state.current_flashcards
            idx   = min(st.session_state.fc_index, len(cards)-1)
            card  = cards[idx]
            total = len(cards)
            prog  = (idx + 1) / total

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
              <div style="flex:1;height:3px;background:#1e2235;border-radius:2px;overflow:hidden;">
                <div style="width:{prog*100:.0f}%;height:100%;
                            background:linear-gradient(90deg,#7c3aed,#67e8f9);border-radius:2px;"></div>
              </div>
              <div style="font-size:0.72rem;font-family:'JetBrains Mono',monospace;color:#475569;white-space:nowrap;">
                {idx+1} / {total}
              </div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1535cc,#0c1a2ecc);
                        border:1px solid #7c3aed40;border-radius:16px;
                        padding:36px 32px;min-height:220px;
                        box-shadow:0 0 40px #7c3aed15,0 8px 32px #00000060;
                        backdrop-filter:blur(12px);margin-bottom:16px;
                        position:relative;overflow:hidden;">
              <div style="position:absolute;top:-40px;right:-40px;width:120px;height:120px;
                          background:radial-gradient(circle,#7c3aed20,transparent 70%);
                          border-radius:50%;pointer-events:none;"></div>
              <div style="font-size:0.65rem;font-family:'JetBrains Mono',monospace;
                          color:#7c3aed;letter-spacing:.12em;margin-bottom:16px;">QUESTION</div>
              <div style="font-size:1.05rem;color:#e2e8f0;line-height:1.7;font-weight:500;">
                {card.get('question','—')}
              </div>
            </div>""", unsafe_allow_html=True)

            if st.session_state.fc_revealed:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0c2e1acc,#0c1a2ecc);
                            border:1px solid #0e749040;border-radius:16px;
                            padding:28px 32px;
                            box-shadow:0 0 30px #0e749015,0 4px 16px #00000040;
                            backdrop-filter:blur(12px);margin-bottom:16px;">
                  <div style="font-size:0.65rem;font-family:'JetBrains Mono',monospace;
                              color:#0e7490;letter-spacing:.12em;margin-bottom:12px;">ANSWER</div>
                  <div style="font-size:0.95rem;color:#94a3b8;line-height:1.75;">
                    {card.get('answer','—')}
                  </div>
                </div>""", unsafe_allow_html=True)

                st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:10px;">HOW DID YOU DO?</div>', unsafe_allow_html=True)

                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("😰  Hard", use_container_width=True, key="fc_hard"):
                        st.session_state.fc_revealed = False
                        st.rerun()
                    st.markdown('<div style="font-size:0.65rem;color:#475569;text-align:center;margin-top:3px;">Review again</div>', unsafe_allow_html=True)
                with b2:
                    if st.button("👍  Good", use_container_width=True, key="fc_good"):
                        st.session_state.fc_index = min(idx + 1, total - 1)
                        st.session_state.fc_revealed = False
                        st.rerun()
                    st.markdown('<div style="font-size:0.65rem;color:#475569;text-align:center;margin-top:3px;">Next card</div>', unsafe_allow_html=True)
                with b3:
                    if st.button("🎯  Easy", use_container_width=True, key="fc_easy"):
                        st.session_state.fc_index = min(idx + 2, total - 1)
                        st.session_state.fc_revealed = False
                        st.rerun()
                    st.markdown('<div style="font-size:0.65rem;color:#475569;text-align:center;margin-top:3px;">Skip ahead</div>', unsafe_allow_html=True)
            else:
                if st.button("👁  Reveal Answer", type="primary", use_container_width=True, key="fc_reveal"):
                    st.session_state.fc_revealed = True
                    st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            nav1, nav2 = st.columns(2)
            with nav1:
                if idx > 0:
                    if st.button("← Previous", use_container_width=True, key="fc_prev"):
                        st.session_state.fc_index -= 1
                        st.session_state.fc_revealed = False
                        st.rerun()
            with nav2:
                if idx < total - 1:
                    if st.button("Next →", use_container_width=True, key="fc_next"):
                        st.session_state.fc_index += 1
                        st.session_state.fc_revealed = False
                        st.rerun()
                elif idx == total - 1:
                    st.markdown('<div style="text-align:center;padding:8px 0;font-size:0.8rem;color:#86efac;">🎉 Deck complete!</div>', unsafe_allow_html=True)
