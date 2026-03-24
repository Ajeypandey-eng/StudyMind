import streamlit as st
from local_ai import generate_schedule

SESSION_COLORS = {
    "Study":    {"bg": "#1e1535", "border": "#7c3aed", "text": "#c084fc", "dot": "#c084fc"},
    "Review":   {"bg": "#0c1a2e", "border": "#0e7490", "text": "#67e8f9", "dot": "#67e8f9"},
    "Practice": {"bg": "#052e16", "border": "#166534", "text": "#86efac", "dot": "#86efac"},
    "Rest":     {"bg": "#1a1a1a", "border": "#374151", "text": "#94a3b8", "dot": "#94a3b8"},
}

def planner_page():
    st.markdown("""
    <div style="padding:10px 0 20px;">
      <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#475569;
                  letter-spacing:.15em;margin-bottom:8px;">SMART SCHEDULER</div>
      <h1>Study Planner</h1>
      <p style="color:#64748b;font-size:0.88rem;margin-top:4px;">
        Generates a personalized Pomodoro schedule — computed locally, no API needed.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#0f1117;border:1px solid #1e2235;border-radius:12px;padding:24px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:14px;">SCHEDULE PARAMETERS</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        subjects = st.text_input("Subjects to Study", placeholder="e.g., Theory of Computation, DBMS, OS")
    with c2:
        exam_date = st.text_input("Exam Date (YYYY-MM-DD)", placeholder="e.g., 2026-04-30")
    with c3:
        hours = st.number_input("Hours/Day", min_value=1, max_value=12, value=4)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if st.button("📅  Generate Schedule", type="primary"):
        if not subjects or not exam_date:
            st.warning("Please fill in subjects and exam date.")
        else:
            with st.spinner("Building your personalized study schedule..."):
                try:
                    schedule = generate_schedule(subjects, exam_date, hours)
                    st.session_state.current_schedule = schedule
                    st.success(f"✅ Generated {len(schedule)}-day study schedule!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.current_schedule:
        schedule = st.session_state.current_schedule
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        total_hours = sum(s.get("hours", 0) for s in schedule)
        total_pomo  = sum(s.get("pomodoro_count", 0) for s in schedule)
        study_days  = sum(1 for s in schedule if s.get("session_type") != "Rest")

        cols = st.columns(4)
        for col, val, lbl, unit in [
            (cols[0], len(schedule),  "Total Days",   ""),
            (cols[1], study_days,     "Study Days",   ""),
            (cols[2], f"{total_hours}","Total Hours",  "h"),
            (cols[3], total_pomo,     "🍅 Pomodoros", ""),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:#13151f;border:1px solid #1e2235;border-radius:10px;
                            padding:14px;text-align:center;margin-bottom:16px;">
                  <div style="font-size:1.5rem;font-weight:700;color:#c084fc;
                              font-family:'Outfit',sans-serif;">{val}{unit}</div>
                  <div style="font-size:0.72rem;color:#475569;margin-top:2px;">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex;gap:14px;margin-bottom:16px;flex-wrap:wrap;">
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:8px;height:8px;background:#c084fc;border-radius:50%;box-shadow:0 0 5px #c084fc80;"></div>
            <span style="font-size:0.72rem;color:#64748b;">Study</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:8px;height:8px;background:#67e8f9;border-radius:50%;box-shadow:0 0 5px #67e8f980;"></div>
            <span style="font-size:0.72rem;color:#64748b;">Review</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:8px;height:8px;background:#86efac;border-radius:50%;box-shadow:0 0 5px #86efac80;"></div>
            <span style="font-size:0.72rem;color:#64748b;">Practice</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:8px;height:8px;background:#94a3b8;border-radius:50%;"></div>
            <span style="font-size:0.72rem;color:#64748b;">Rest</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.65rem;color:#475569;font-family:\'JetBrains Mono\',monospace;letter-spacing:.1em;margin-bottom:12px;">SCHEDULE</div>', unsafe_allow_html=True)

        for i, session in enumerate(schedule):
            stype  = session.get("session_type", "Study")
            colors = SESSION_COLORS.get(stype, SESSION_COLORS["Study"])
            day    = session.get("day", f"Day {i+1}")
            topic  = session.get("topic", "—")
            hrs    = session.get("hours", 0)
            pomo   = session.get("pomodoro_count", 0)

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:16px;padding:14px 18px;
                        background:{colors['bg']};border:1px solid {colors['border']}40;
                        border-left:3px solid {colors['border']};border-radius:10px;margin-bottom:8px;">
              <div style="flex-shrink:0;text-align:center;min-width:70px;">
                <div style="font-size:0.72rem;font-family:'JetBrains Mono',monospace;
                            color:{colors['dot']};font-weight:600;">{day.split(' - ')[0] if ' - ' in day else day}</div>
                <div style="font-size:0.62rem;color:#334155;margin-top:1px;">
                  {day.split(' - ')[1] if ' - ' in day else ''}
                </div>
              </div>
              <div style="width:1px;height:32px;background:#1e2235;flex-shrink:0;"></div>
              <div style="flex:1;min-width:0;">
                <div style="font-size:0.88rem;color:#e2e8f0;font-weight:500;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{topic}</div>
                <div style="margin-top:4px;">
                  <span style="font-size:0.68rem;font-family:'JetBrains Mono',monospace;
                               color:{colors['text']};background:{colors['bg']};
                               border:1px solid {colors['border']}50;padding:1px 7px;border-radius:4px;">
                    {stype}
                  </span>
                </div>
              </div>
              <div style="display:flex;gap:20px;flex-shrink:0;text-align:center;">
                <div>
                  <div style="font-size:1rem;font-weight:700;color:{colors['dot']};font-family:'Outfit',sans-serif;">{hrs}h</div>
                  <div style="font-size:0.62rem;color:#475569;">hours</div>
                </div>
                <div>
                  <div style="font-size:1rem;font-weight:700;color:#f97316;font-family:'Outfit',sans-serif;">🍅{pomo}</div>
                  <div style="font-size:0.62rem;color:#475569;">pomodoros</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("🗑 Clear Schedule", type="secondary"):
            st.session_state.current_schedule = []
            st.rerun()
