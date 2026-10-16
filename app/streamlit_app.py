
import sys
import re
import json
import hashlib
import tempfile
from pathlib import Path

import streamlit as st
import chromadb

# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
VECTOR_DB_PATH = PROJECT_ROOT / "vector_store"
MANIFEST_PATH = PROJECT_ROOT / "uploaded_documents_manifest.json"
COLLECTION_NAME = "project_documents"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from document_processor import process_documents
from multi_document_chunking import process_and_chunk_documents
from embeddings import create_embeddings
from vector_store import create_vector_store
from scope_agent import extract_scope_and_deliverables
from risk_delivery_agent import detect_risks_and_forecast_delivery
from blocker_action_agent import identify_blockers_and_action_items
from documentation_agent import generate_project_documentation
from project_health import calculate_project_health
from conversational_assistant import ask_project_assistant

st.set_page_config(
    page_title="ProjectPilot | AI Project Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. KNOWLEDGE BASE INITIALIZATION
# ============================================================

@st.cache_resource
def initialize_fresh_server():
    """Clear the previous collection when the server initializes."""
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    if MANIFEST_PATH.exists():
        MANIFEST_PATH.unlink()

    return True


try:
    initialize_fresh_server()
except Exception as error:
    st.error(f"Knowledge base initialization failed: {error}")
    st.stop()

# ============================================================
# 3. SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "document_names": [],
    "document_hashes": {},
    "uploaded_documents": [],
    "uploader_version": 0,
    "upload_status_message": None,
    "scope_result": None,
    "risk_result": None,
    "blocker_result": None,
    "health_result": None,
    "documentation_result": None,
    "assistant_messages": [],
    "agent_errors": {},
    "analysis_completed": False,
    "main_navigation": "Dashboard",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# 4. DARK THEME — HIGH CONTRAST
# ============================================================

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #0B1120 !important;
        color: #F8FAFC !important;
    }

    [data-testid="stHeader"] {
        background: #0B1120 !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {
        background: #111827 !important;
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #334155 !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, li,
    [data-testid="stMarkdownContainer"],
    [data-testid="stCaptionContainer"] {
        color: #F1F5F9;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }

    .main-title {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .subtitle {
        color: #CBD5E1 !important;
        font-size: 0.97rem;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }

    .eyebrow {
        color: #93C5FD !important;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .hero {
        background: linear-gradient(120deg, #172554, #111827);
        border: 1px solid #475569;
        border-radius: 18px;
        padding: 1.5rem;
        margin: 0.7rem 0 1.4rem;
    }

    .hero h2 {
        color: #FFFFFF !important;
        font-size: 1.7rem;
    }

    .hero p {
        color: #E2E8F0 !important;
        line-height: 1.7;
    }

    /* Sidebar navigation */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        min-height: 3rem !important;
        background: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        border-radius: 11px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.65rem 0.85rem !important;
        font-weight: 650 !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] .stButton > button *,
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #334155 !important;
        border-color: #93C5FD !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #2563EB !important;
        border-color: #93C5FD !important;
    }

    /* Main buttons */
    [data-testid="stMain"] .stButton > button,
    [data-testid="stDownloadButton"] button {
        background: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #64748B !important;
        border-radius: 10px !important;
        font-weight: 650 !important;
        opacity: 1 !important;
    }

    [data-testid="stMain"] .stButton > button *,
    [data-testid="stDownloadButton"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stMain"] .stButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: #334155 !important;
        border-color: #93C5FD !important;
    }

    [data-testid="stMain"] .stButton > button[kind="primary"] {
        background: #2563EB !important;
        border-color: #93C5FD !important;
    }

    /* ========================================================
       ASSISTANT LAUNCHER — FIX WHITE BUTTON / INVISIBLE TEXT
       ======================================================== */

    [data-testid="stPopover"] button,
    [data-testid="stPopover"] > div > button,
    button[data-testid="stPopoverButton"] {
        background: #1E293B !important;
        background-color: #1E293B !important;
        background-image: none !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #64748B !important;
        border-radius: 10px !important;
        opacity: 1 !important;
        box-shadow: none !important;
    }

    [data-testid="stPopover"] button *,
    [data-testid="stPopover"] button p,
    [data-testid="stPopover"] button span,
    [data-testid="stPopover"] button div,
    [data-testid="stPopover"] button svg,
    button[data-testid="stPopoverButton"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    [data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: #334155 !important;
        background-color: #334155 !important;
        border-color: #93C5FD !important;
    }

    /* Open assistant panel */
    [data-testid="stPopoverBody"],
    [data-testid="stPopoverBody"] > div,
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlock"],
    [data-testid="stPopoverBody"] [data-testid="stForm"] {
        background: #111827 !important;
        background-color: #111827 !important;
        color: #F8FAFC !important;
    }

    [data-testid="stPopoverBody"] h1,
    [data-testid="stPopoverBody"] h2,
    [data-testid="stPopoverBody"] h3,
    [data-testid="stPopoverBody"] p,
    [data-testid="stPopoverBody"] label,
    [data-testid="stPopoverBody"] span,
    [data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] {
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }

    /* Inputs: dark background, white text, readable placeholder */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        background: #1E293B !important;
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #64748B !important;
        border-radius: 9px !important;
        caret-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder,
    [data-baseweb="input"] input::placeholder,
    [data-baseweb="textarea"] textarea::placeholder {
        color: #CBD5E1 !important;
        -webkit-text-fill-color: #CBD5E1 !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stFileUploader"] label {
        color: #F8FAFC !important;
    }

    /* Assistant submit button */
    [data-testid="stPopoverBody"] [data-testid="stFormSubmitButton"] button,
    [data-testid="stPopoverBody"] [data-testid="stForm"] button,
    [data-testid="stFormSubmitButton"] button {
        background: #2563EB !important;
        background-color: #2563EB !important;
        background-image: none !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #93C5FD !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    [data-testid="stPopoverBody"] [data-testid="stFormSubmitButton"] button *,
    [data-testid="stPopoverBody"] [data-testid="stForm"] button *,
    [data-testid="stFormSubmitButton"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    [data-testid="stPopoverBody"] [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stPopoverBody"] [data-testid="stForm"] button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background: #1D4ED8 !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #111827 !important;
        border: 1px dashed #64748B !important;
        border-radius: 14px !important;
        padding: 0.8rem !important;
    }

    [data-testid="stFileUploader"] section {
        background: #111827 !important;
        color: #F8FAFC !important;
    }

    [data-testid="stFileUploader"] button {
        background: #334155 !important;
        color: #FFFFFF !important;
        border: 1px solid #64748B !important;
        border-radius: 8px !important;
        opacity: 1 !important;
    }

    [data-testid="stFileUploader"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span {
        color: #E2E8F0 !important;
    }

    /* Metrics and containers */
    [data-testid="stMetric"] {
        background: #111827 !important;
        border: 1px solid #475569 !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 15px !important;
    }

    [data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #F8FAFC !important;
    }

    [data-testid="stSelectbox"] div,
    [data-baseweb="select"] > div {
        color: #FFFFFF !important;
    }

    [role="listbox"],
    [role="option"] {
        background: #1E293B !important;
        color: #FFFFFF !important;
    }

    /* Progress bars */
    [data-testid="stProgress"] > div {
        background: #334155 !important;
        border-radius: 20px !important;
        overflow: hidden !important;
    }

    [data-testid="stProgress"] > div > div {
        border-radius: 20px !important;
    }

    /* Tabs, links, alerts and dividers */
    [data-testid="stTabs"] button {
        color: #CBD5E1 !important;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #93C5FD !important;
        border-bottom-color: #60A5FA !important;
    }

    a { color: #93C5FD !important; }
    a:hover { color: #BFDBFE !important; }

    [data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    [data-testid="stAlert"] p {
        color: #FFFFFF !important;
    }

    hr { border-color: #334155 !important; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def get_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


def save_manifest(data):
    temporary_path = MANIFEST_PATH.with_suffix(".tmp")
    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    temporary_path.replace(MANIFEST_PATH)


def reset_analysis_results():
    for key in [
        "scope_result",
        "risk_result",
        "blocker_result",
        "health_result",
        "documentation_result",
    ]:
        st.session_state[key] = None

    st.session_state.assistant_messages = []
    st.session_state.agent_errors = {}
    st.session_state.analysis_completed = False


def make_preview(result, max_lines=6, max_chars=850):
    if not result:
        return "No results available yet."

    lines = []
    for line in str(result).splitlines():
        line = line.strip()
        if line:
            lines.append(line)
        if len(lines) >= max_lines:
            break

    preview = "\n\n".join(lines)
    if len(preview) > max_chars:
        preview = preview[:max_chars].rstrip() + "..."

    return preview or "No preview available."


def extract_score(text, section=None):
    """Extract a score from the labelled report section."""
    if not text:
        return None

    text = str(text)

    if section:
        patterns = [
            rf"###\s*\d+\.\s*{re.escape(section)}(.*?)(?=###\s*\d+\.|\Z)",
            rf"(?im)^\s*{re.escape(section)}\s*$"
            rf"(.*?)(?=^\s*\d+\.\s|\Z)",
        ]

        section_text = None
        for pattern in patterns:
            match = re.search(
                pattern, text, re.IGNORECASE | re.DOTALL | re.MULTILINE
            )
            if match:
                section_text = match.group(1)
                break

        if section_text is None:
            return None

        match = re.search(
            r"\*{0,2}Score:\*{0,2}\s*(\d{1,3})\s*/\s*100",
            section_text,
            re.IGNORECASE,
        )

        if not match:
            match = re.search(
                r"\bScore\s*:\s*(\d{1,3})\s*/\s*100",
                section_text,
                re.IGNORECASE,
            )
    else:
        match = re.search(
            r"Overall Score:\s*(\d{1,3})\s*/\s*100",
            text,
            re.IGNORECASE,
        )

        if not match:
            match = re.search(
                r"Overall Health Score:\s*(\d{1,3})\s*/\s*100",
                text,
                re.IGNORECASE,
            )

    if match:
        score = int(match.group(1))
        if 0 <= score <= 100:
            return score

    return None


def display_health_report(report):
    if not report:
        st.info("Calculate project health to generate the report.")
        return

    report_text = str(report)
    overall_score = extract_score(report_text)

    st.markdown("### Overall Project Health")

    if overall_score is not None:
        st.markdown(f"**Overall Score: {overall_score}/100**")
        st.progress(overall_score / 100)

        if overall_score >= 80:
            st.success("Project status: Healthy")
        elif overall_score >= 60:
            st.warning("Project status: Moderate")
        else:
            st.error("Project status: Needs Attention")
    else:
        st.warning(
            "The report does not contain a clearly labelled overall score. "
            "Expected format: Overall Score: 70/100."
        )

    st.markdown("### Health Statistics")

    scope_score = extract_score(report_text, "Scope Clarity")
    timeline_score = extract_score(report_text, "Timeline Risk")

    if scope_score is not None:
        st.markdown(f"**Scope Clarity — {scope_score}/100**")
        st.progress(scope_score / 100)

    if timeline_score is not None:
        st.markdown(f"**Timeline Risk — {timeline_score}/100**")
        st.progress(timeline_score / 100)

    st.markdown("---")
    st.markdown("### Full Health Assessment")
    st.markdown(report_text)


def display_saved_documents():
    names = sorted(st.session_state.document_names)

    if not names:
        st.info("No documents have been indexed in this session.")
        return

    for index, name in enumerate(names, start=1):
        st.markdown(f"{index}. 📄 `{name}`")


def display_result_preview(title, result):
    st.markdown(f"### {title}")

    if not result:
        st.info("No result available yet.")
        return

    st.markdown(make_preview(result))

    with st.expander("View complete report"):
        st.markdown(str(result))


def run_all_agents():
    agents = [
        ("scope_result", "Scope Analysis", extract_scope_and_deliverables),
        ("risk_result", "Risk and Delivery Analysis", detect_risks_and_forecast_delivery),
        ("blocker_result", "Blocker and Action Item Analysis", identify_blockers_and_action_items),
    ]

    st.session_state.agent_errors = {}
    progress = st.progress(0)
    status = st.empty()

    for index, (key, label, function) in enumerate(agents):
        status.info(f"Running {label}...")

        try:
            result = function()
            if result is None:
                st.session_state[key] = None
                st.session_state.agent_errors[label] = (
                    "The agent returned no result."
                )
            else:
                st.session_state[key] = str(result)
        except Exception as error:
            st.session_state[key] = None
            st.session_state.agent_errors[label] = str(error)

        progress.progress((index + 1) / len(agents))

    status.empty()
    progress.empty()

    st.session_state.analysis_completed = any(
        st.session_state[key]
        for key in ["scope_result", "risk_result", "blocker_result"]
    )


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

NAV_ITEMS = [
    ("Dashboard", "📊"),
    ("Documents", "📂"),
    ("AI Agents", "🤖"),
    ("Documentation Generator", "📝"),
    ("Project Health", "❤️"),
]

with st.sidebar:
    st.markdown("## 🚀 ProjectPilot")
    st.caption("AI-Powered Project Intelligence")
    st.divider()
    st.markdown("### WORKSPACE")

    for destination, icon in NAV_ITEMS:
        if st.button(
            f"{icon}  {destination}",
            key=f"nav_{destination}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.main_navigation == destination
                else "secondary"
            ),
        ):
            st.session_state.main_navigation = destination
            st.rerun()

    st.divider()
    st.markdown("### PROJECT STATUS")
    st.metric("Indexed Documents", len(st.session_state.document_names))

    if st.session_state.analysis_completed:
        st.success("AI analysis completed")
    else:
        st.info("Analysis not completed")

    st.divider()
    st.markdown("### SUPPORTED FORMATS")
    st.caption("PDF · DOCX · CSV · TXT")


# ============================================================
# 7. APPLICATION HEADER
# ============================================================

st.markdown(
    '<div class="eyebrow">PROJECT INTELLIGENCE PLATFORM</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">AI Project Intelligence & Risk Advisor</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Understand project scope, review delivery risks, track blockers, '
    'and make informed project decisions.'
    '</div>',
    unsafe_allow_html=True,
)

page = st.session_state.main_navigation


# ============================================================
# 8. DASHBOARD
# ============================================================

if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">PROJECT OVERVIEW</div>
            <h2>Your Project Intelligence Dashboard</h2>
            <p>
                Review your knowledge base, project health,
                AI-generated insights, delivery risks, and actions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📁 Documents", len(st.session_state.document_names))
    col2.metric(
        "🎯 Scope Analysis",
        "Ready" if st.session_state.scope_result else "Pending",
    )
    col3.metric(
        "⚠️ Risk Analysis",
        "Ready" if st.session_state.risk_result else "Pending",
    )
    col4.metric(
        "🚧 Blocker Analysis",
        "Ready" if st.session_state.blocker_result else "Pending",
    )

    st.markdown("---")
    st.markdown("## ❤️ Project Health")

    if st.session_state.health_result:
        display_health_report(st.session_state.health_result)
    else:
        st.info("Calculate project health to display the overall score and report.")
        if st.button(
            "Calculate Project Health",
            type="primary",
            key="dashboard_calculate_health",
        ):
            st.session_state.main_navigation = "Project Health"
            st.rerun()

    st.markdown("---")
    st.markdown("## 🧠 AI-Generated Project Insights")

    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            display_result_preview(
                "🎯 Scope & Deliverables",
                st.session_state.scope_result,
            )

    with right:
        with st.container(border=True):
            display_result_preview(
                "⚠️ Risk & Delivery",
                st.session_state.risk_result,
            )

    with st.container(border=True):
        display_result_preview(
            "🚧 Blockers & Action Items",
            st.session_state.blocker_result,
        )

    st.markdown("---")
    st.markdown("## 📝 Documentation Status")

    if st.session_state.documentation_result:
        st.success("Project documentation has been generated.")
        st.download_button(
            "Download Project Documentation",
            data=str(st.session_state.documentation_result),
            file_name="project_documentation.txt",
            mime="text/plain",
            key="dashboard_download_documentation",
        )
    else:
        st.info(
            "Documentation has not been generated yet. "
            "Open Documentation Generator in the sidebar."
        )

    st.markdown("---")
    st.markdown("## 📚 Indexed Knowledge Base")

    if st.session_state.document_names:
        with st.container(border=True):
            display_saved_documents()
    else:
        st.info("No documents are indexed. Open Documents to upload files.")


# ============================================================
# 9. DOCUMENT MANAGEMENT
# ============================================================

elif page == "Documents":
    st.markdown("## 📂 Project Document Management")
    st.write(
        "Upload project documents to create your searchable knowledge "
        "base. New or modified files are processed incrementally."
    )

    uploaded_files = st.file_uploader(
        "Upload project documents",
        type=["pdf", "docx", "csv", "txt"],
        accept_multiple_files=True,
        key=f"document_uploader_{st.session_state.uploader_version}",
        help="Supported formats: PDF, DOCX, CSV, and TXT.",
    )

    if st.session_state.upload_status_message:
        st.success(st.session_state.upload_status_message)
        st.session_state.upload_status_message = None

    if uploaded_files:
        files_to_process = []
        pending_hashes = {}

        for uploaded_file in uploaded_files:
            content = uploaded_file.getvalue()
            file_hash = get_file_hash(content)

            if st.session_state.document_hashes.get(uploaded_file.name) != file_hash:
                files_to_process.append(uploaded_file)
                pending_hashes[uploaded_file.name] = file_hash

        if not files_to_process:
            st.success("All selected documents are already indexed and unchanged.")
        else:
            with st.spinner("Extracting text, creating embeddings, and indexing..."):
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_path = Path(temp_dir)

                        for uploaded_file in files_to_process:
                            destination = temp_path / uploaded_file.name
                            destination.write_bytes(uploaded_file.getvalue())

                        processed_documents = process_documents(str(temp_path))
                        chunks = process_and_chunk_documents(str(temp_path))

                        if not chunks:
                            raise ValueError(
                                "No text chunks were generated. "
                                "Check whether the files contain extractable text."
                            )

                        chunk_texts = [
                            str(chunk.get("text", ""))
                            if isinstance(chunk, dict)
                            else str(chunk)
                            for chunk in chunks
                        ]

                        if not all(text.strip() for text in chunk_texts):
                            raise ValueError("Some chunks contain empty text.")

                        embeddings = create_embeddings(chunk_texts)

                        if len(chunks) != len(embeddings):
                            raise ValueError(
                                "The number of chunks and embeddings does not match."
                            )

                        collection = create_vector_store(chunks, embeddings)

                    updated_hashes = dict(st.session_state.document_hashes)
                    updated_hashes.update(pending_hashes)
                    save_manifest(updated_hashes)

                    st.session_state.document_hashes = updated_hashes
                    st.session_state.document_names = sorted(updated_hashes.keys())

                    if isinstance(processed_documents, list):
                        st.session_state.uploaded_documents.extend(processed_documents)
                    elif processed_documents:
                        st.session_state.uploaded_documents.append(processed_documents)

                    reset_analysis_results()

                    st.session_state.upload_status_message = (
                        f"Successfully indexed {len(files_to_process)} "
                        f"document(s). Collection contains {collection.count()} chunks."
                    )

                    st.session_state.uploader_version += 1
                    st.rerun()

                except Exception as error:
                    st.error(f"Document processing failed: {error}")

    st.markdown("---")
    st.markdown("### 📚 Indexed Documents")
    display_saved_documents()

    st.markdown("---")
    st.markdown("### 🚀 Project Analysis")
    st.write(
        "Run the three agents to analyze scope, risks, blockers, "
        "and recommended actions."
    )

    if st.button(
        "Run Project Analysis",
        type="primary",
        use_container_width=True,
        disabled=not bool(st.session_state.document_names),
    ):
        run_all_agents()
        if st.session_state.analysis_completed:
            st.success("Analysis completed. Visit Dashboard or AI Agents.")
        else:
            st.error("No agent produced a result. Check the errors below.")

    for name, error in st.session_state.agent_errors.items():
        st.error(f"{name}: {error}")


# ============================================================
# 10. AI AGENTS
# ============================================================

elif page == "AI Agents":
    st.markdown("## 🤖 Project Analysis Agents")

    tab1, tab2, tab3 = st.tabs([
        "🎯 Scope & Deliverables",
        "⚠️ Risk & Delivery",
        "🚧 Blockers & Actions",
    ])

    with tab1:
        if st.session_state.scope_result:
            st.markdown(str(st.session_state.scope_result))
        else:
            st.info("Run Project Analysis from Documents to generate the scope report.")

    with tab2:
        if st.session_state.risk_result:
            st.markdown(str(st.session_state.risk_result))
        else:
            st.info("Run Project Analysis from Documents to generate the risk report.")

    with tab3:
        if st.session_state.blocker_result:
            st.markdown(str(st.session_state.blocker_result))
        else:
            st.info("Run Project Analysis from Documents to identify blockers.")

    if st.session_state.agent_errors:
        st.markdown("---")
        st.markdown("### Agent Errors")
        for name, error in st.session_state.agent_errors.items():
            st.error(f"{name}: {error}")


# ============================================================
# 11. DOCUMENTATION GENERATOR
# ============================================================

elif page == "Documentation Generator":
    st.markdown("## 📝 Project Documentation Generator")
    st.write("Generate documentation using your indexed project knowledge.")

    if st.button(
        "Generate Project Documentation",
        type="primary",
        use_container_width=True,
        disabled=not bool(st.session_state.document_names),
    ):
        with st.spinner("Generating project documentation..."):
            try:
                result = generate_project_documentation()

                if result is None:
                    st.warning("The documentation generator returned no result.")
                else:
                    st.session_state.documentation_result = str(result)
                    st.success("Documentation generated successfully.")

            except Exception as error:
                st.error(f"Documentation generation failed: {error}")

    if st.session_state.documentation_result:
        st.markdown("---")
        st.markdown("### Generated Documentation")
        st.markdown(str(st.session_state.documentation_result))

        st.download_button(
            "Download Documentation",
            data=str(st.session_state.documentation_result),
            file_name="project_documentation.txt",
            mime="text/plain",
            use_container_width=True,
            key="documentation_download_button",
        )


# ============================================================
# 12. PROJECT HEALTH
# ============================================================

elif page == "Project Health":
    st.markdown("## ❤️ Project Health")
    st.write(
        "Calculate the overall project health score, review scope clarity, "
        "timeline risk, blockers, and the overall assessment."
    )

    if st.button(
        "Calculate Project Health",
        type="primary",
        use_container_width=True,
        disabled=not bool(st.session_state.document_names),
    ):
        with st.spinner("Calculating project health..."):
            try:
                result = calculate_project_health()

                if result is None:
                    st.session_state.health_result = None
                    st.warning("The health function returned no result.")
                else:
                    st.session_state.health_result = str(result)
                    st.success("Health assessment generated.")

            except Exception as error:
                st.error(f"Health calculation failed: {error}")

    if st.session_state.health_result:
        st.markdown("---")
        display_health_report(st.session_state.health_result)

        st.download_button(
            "Download Health Report",
            data=str(st.session_state.health_result),
            file_name="project_health_report.txt",
            mime="text/plain",
            use_container_width=True,
            key="health_report_download_button",
        )


# ============================================================
# 13. PROJECT ASSISTANT
# ============================================================

st.markdown("---")

with st.popover("💬 Ask Project Assistant", use_container_width=True):
    st.markdown("### Project Assistant")
    st.caption("Ask questions about the indexed project documents.")

    with st.form("project_assistant_form", clear_on_submit=True):
        question = st.text_input(
            "Your question",
            placeholder="What are the main project risks?",
        )

        submitted = st.form_submit_button(
            "Ask Assistant",
            use_container_width=True,
        )

    if submitted:
        if not question.strip():
            st.warning("Please enter a question.")
        elif not st.session_state.document_names:
            st.warning("Upload project documents first.")
        else:
            with st.spinner("Searching project knowledge..."):
                try:
                    answer = ask_project_assistant(question.strip())
                    answer = (
                        str(answer)
                        if answer is not None
                        else "The assistant returned no answer."
                    )

                    st.session_state.assistant_messages.append({
                        "question": question.strip(),
                        "answer": answer,
                    })

                except Exception as error:
                    st.error(f"Assistant request failed: {error}")

    for message in reversed(st.session_state.assistant_messages):
        st.markdown("**Question**")
        st.write(message["question"])
        st.markdown("**Answer**")
        st.markdown(message["answer"])
        st.divider()


# ============================================================
# 14. FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#CBD5E1;
        font-size:0.8rem;
        padding:1.5rem 0;
    ">
        <strong>ProjectPilot</strong><br>
        AI Project Intelligence & Risk Advisor
    </div>
    """,
    unsafe_allow_html=True,
)
