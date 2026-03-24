import streamlit as st

st.set_page_config(
    page_title="StudyMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #080a10 !important;
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
}

#MainMenu, footer { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
.stDeployButton { display: none !important; }
header { background-color: transparent !important; }

[data-testid="stSidebar"] {
    background: #0c0e18 !important;
    border-right: 1px solid #1e2235 !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

[data-testid="stMainBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
.main .block-container { padding: 24px 28px !important; max-width: 100% !important; }

h1 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.75rem !important;
    background: linear-gradient(135deg, #c084fc, #67e8f9) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 4px !important;
}
h2, h3 { font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; color: #c4b5fd !important; }

.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    border: 1px solid #2d2f45 !important;
    background: #13151f !important;
    color: #94a3b8 !important;
    transition: all 0.2s ease !important;
    padding: 8px 16px !important;
}
.stButton > button:hover {
    background: #1e2035 !important;
    border-color: #7c3aed !important;
    color: #c084fc !important;
    box-shadow: 0 0 12px #7c3aed30 !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #0e7490) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 15px #7c3aed40 !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 25px #7c3aed70 !important;
    transform: translateY(-1px) !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #13151f !important;
    border: 1px solid #1e2235 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px #7c3aed30 !important;
}

[data-testid="stChatMessageContent"] {
    background: #13151f !important;
    border: 1px solid #1e2235 !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stChatInput"] textarea {
    background: #13151f !important;
    border: 1px solid #2d2f45 !important;
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px #7c3aed30 !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #7c3aed, #0e7490) !important;
    border-radius: 8px !important;
}

.streamlit-expanderHeader {
    background: #13151f !important;
    border: 1px solid #1e2235 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}
.streamlit-expanderContent {
    background: #0f1117 !important;
    border: 1px solid #1e2235 !important;
    border-top: none !important;
}

[data-testid="stFileUploader"] {
    background: #0f1117 !important;
    border: 2px dashed #2d2f45 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c3aed !important;
    background: #13151f !important;
}

[data-testid="stAlert"] { border-radius: 10px !important; font-family: 'Outfit', sans-serif !important; }
.stSuccess { background: #052e16 !important; border: 1px solid #166534 !important; }
.stWarning { background: #1c1400 !important; border: 1px solid #854d0e !important; }
.stInfo    { background: #0c1a2e !important; border: 1px solid #1e40af !important; }

hr { border-color: #1e2235 !important; }
.stNumberInput button { background: #1e2235 !important; border-color: #2d2f45 !important; color: #94a3b8 !important; }
.stSpinner > div { border-color: #7c3aed !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080a10; }
::-webkit-scrollbar-thumb { background: #2d2f45; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #7c3aed; }

.stCaption { color: #475569 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important; }

[data-testid="stMetric"] {
    background: #13151f !important;
    border: 1px solid #1e2235 !important;
    border-radius: 10px !important;
    padding: 14px !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #c084fc !important; font-size: 1.6rem !important; font-weight: 700 !important; }

[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "page": "home",
    "documents": {},
    "chat_history": [],
    "current_flashcards": [],
    "current_schedule": [],
    "fc_index": 0,
    "fc_revealed": False,
    "models_loaded": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Warm up models in background on first load ────────────────────────────────
if not st.session_state.models_loaded:
    with st.spinner("⚙️ Loading local AI models (first launch only — ~30 seconds)..."):
        from local_ai import load_embedder, load_generator
        load_embedder()
        load_generator()
        st.session_state.models_loaded = True

# ── Routing ───────────────────────────────────────────────────────────────────
from components.sidebar import sidebar
from pages.home       import home_page
from pages.upload     import upload_page
from pages.qa         import qa_page
from pages.flashcards import flashcards_page
from pages.planner    import planner_page

sidebar()

page = st.session_state.page
if   page == "home":       home_page()
elif page == "upload":     upload_page()
elif page == "qa":         qa_page()
elif page == "flashcards": flashcards_page()
elif page == "planner":    planner_page()
