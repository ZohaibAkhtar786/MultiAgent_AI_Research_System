import streamlit as st
from pipeline import run_research_pipeline

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    
    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 { font-size: 2.4rem; font-weight: 700; margin: 0 0 0.5rem 0; }
    .hero p  { font-size: 1.05rem; opacity: 0.8; margin: 0; }

    /* Pipeline badges */
    .pipeline-row {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin: 1.2rem 0 2rem 0;
    }
    .badge {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 999px;
        padding: 0.35rem 1rem;
        font-size: 0.82rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Section cards */
    .section-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-divider {
        border: none;
        border-top: 1px solid #1e293b;
        margin: 0.8rem 0;
    }

    /* Score pill */
    .score-pill {
        display: inline-block;
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        border-radius: 999px;
        padding: 0.3rem 1.2rem;
        margin-bottom: 1rem;
    }

    /* Input area */
    .stTextInput > div > div > input {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-size: 1rem !important;
        padding: 0.7rem 1rem !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: opacity 0.2s;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.88 !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1e293b !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #1e293b;
        border-radius: 10px;
        gap: 4px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #4f46e5 !important;
        color: white !important;
    }

    /* Status message */
    .status-success {
        background: #052e16;
        border: 1px solid #166534;
        border-radius: 10px;
        padding: 0.7rem 1.2rem;
        color: #4ade80;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    .status-error {
        background: #2d0a0a;
        border: 1px solid #991b1b;
        border-radius: 10px;
        padding: 0.7rem 1.2rem;
        color: #f87171;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""
if "error" not in st.session_state:
    st.session_state.error = None

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧠 Multi-Agent Research System</h1>
    <p>Powered by LangChain · GPT-4o mini · Tavily Search · BeautifulSoup</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pipeline-row">
    <span class="badge">🔍 Search Agent</span>
    <span class="badge">→</span>
    <span class="badge">📄 Reader Agent</span>
    <span class="badge">→</span>
    <span class="badge">✍️ Writer Chain</span>
    <span class="badge">→</span>
    <span class="badge">🧠 Critical Thinking Chain</span>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g. The impact of artificial intelligence on healthcare in 2025",
        label_visibility="collapsed",
    )
with col2:
    run_btn = st.button("🚀 Run Research", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Run Pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown('<div class="status-error">⚠️ Please enter a research topic before running.</div>', unsafe_allow_html=True)
    else:
        st.session_state.error = None
        st.session_state.results = None
        st.session_state.last_topic = topic.strip()

        with st.spinner("🔄 Running the research pipeline — this may take a minute..."):
            try:
                results = run_research_pipeline(topic.strip())
                st.session_state.results = results
            except Exception as e:
                st.session_state.error = str(e)

# ── Error Display ─────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="status-error">❌ An error occurred: {st.session_state.error}</div>',
        unsafe_allow_html=True,
    )

# ── Results Display ───────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    st.markdown(
        f'<div class="status-success">✅ Research completed for: <strong>{st.session_state.last_topic}</strong></div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Search Results",
        "📄 Scraped Content",
        "📝 Research Report",
        "🧠 Critical Feedback",
    ])

    # ── Tab 1: Search Results ─────────────────────────────────────────────────
    with tab1:
        st.markdown("### 🔍 Search Results")
        st.caption("Raw results gathered by the Search Agent via Tavily.")
        st.markdown("---")
        search_blocks = r.get("search_results", "No search results available.").split(
            "------------------------------------------------------------"
        )
        for i, block in enumerate(search_blocks, 1):
            block = block.strip()
            if block:
                with st.expander(f"Result {i}", expanded=(i == 1)):
                    st.markdown(block)

    # ── Tab 2: Scraped Content ────────────────────────────────────────────────
    with tab2:
        st.markdown("### 📄 Scraped Content")
        st.caption("Deep content extracted by the Reader Agent from the most relevant URL.")
        st.markdown("---")
        scraped = r.get("scraped_content", "No scraped content available.")
        with st.expander("View Full Scraped Text", expanded=True):
            st.text(scraped)

    # ── Tab 3: Research Report ────────────────────────────────────────────────
    with tab3:
        st.markdown("### 📝 Research Report")
        st.caption("Structured report generated by the Writer Chain.")
        st.markdown("---")
        report = r.get("research_report", "No report available.")
        st.markdown(report)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Report as .txt",
            data=report,
            file_name=f"research_report_{st.session_state.last_topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
        )

    # ── Tab 4: Critical Feedback ──────────────────────────────────────────────
    with tab4:
        st.markdown("### 🧠 Critical Feedback")
        st.caption("Evaluation and critique produced by the Critical Thinking Chain.")
        st.markdown("---")
        feedback = r.get("critical_feedback", "No feedback available.")

        # Try to extract and highlight the score
        score_line = ""
        remaining_lines = []
        for line in feedback.splitlines():
            if line.strip().lower().startswith("score:"):
                score_line = line.strip().replace("Score:", "").strip()
            else:
                remaining_lines.append(line)

        if score_line:
            st.markdown(f'<div class="score-pill">Score: {score_line}</div>', unsafe_allow_html=True)

        st.markdown("\n".join(remaining_lines))
