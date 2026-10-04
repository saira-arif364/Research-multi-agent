import streamlit as st
import re
import traceback

from crew import build_crew


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Research AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "current_agent" not in st.session_state:
    st.session_state.current_agent = None

if "agent_states" not in st.session_state:
    st.session_state.agent_states = {
        "Researcher": "waiting",
        "Fact Checker": "waiting",
        "Analyst": "waiting",
        "Writer": "waiting",
    }

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "running" not in st.session_state:
    st.session_state.running = False


AGENTS = [
    "Researcher",
    "Fact Checker",
    "Analyst",
    "Writer",
]


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(52, 152, 219, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(155, 89, 182, 0.08),
                transparent 30%
            ),
            #080b12;
        color: #f4f7fb;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main container */
    .block-container {
        max-width: 1180px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* Brand */
    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 8px;
    }

    .brand-icon {
        width: 48px;
        height: 48px;
        border-radius: 15px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: linear-gradient(
            135deg,
            #35d9ff,
            #7367ff
        );

        color: white;
        font-size: 25px;
        font-weight: 700;

        box-shadow:
            0 0 30px rgba(53, 217, 255, 0.22);
    }

    .brand-title {
        font-size: 31px;
        font-weight: 750;
        letter-spacing: -0.7px;
    }

    .brand-subtitle {
        color: #8d99aa;
        font-size: 14px;
        margin-top: 2px;
    }

    /* Hero */
    .hero {
        margin-top: 42px;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 44px;
        line-height: 1.1;
        font-weight: 780;
        letter-spacing: -1.5px;
        margin-bottom: 12px;
    }

    .hero-title span {
        background: linear-gradient(
            90deg,
            #35d9ff,
            #8b7cff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        color: #98a4b5;
        font-size: 17px;
        max-width: 720px;
        line-height: 1.65;
    }

    /* Input label */
    .input-label {
        color: #dce4ee;
        font-size: 14px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    /* Text area */
    textarea {
        background: #10151e !important;
        color: #f5f7fb !important;
        border: 1px solid #263142 !important;
        border-radius: 14px !important;
    }

    textarea:focus {
        border-color: #35d9ff !important;
        box-shadow: 0 0 0 1px #35d9ff33 !important;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        height: 52px;

        border: none;
        border-radius: 14px;

        background: linear-gradient(
            90deg,
            #24c8f4,
            #7165ff
        );

        color: white;
        font-size: 15px;
        font-weight: 700;

        box-shadow:
            0 8px 28px rgba(52, 167, 255, 0.18);

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 12px 35px rgba(52, 167, 255, 0.28);
    }

    /* Agent workflow */
    .workflow-title {
        font-size: 18px;
        font-weight: 700;
        margin-top: 42px;
        margin-bottom: 14px;
    }

    .agent-grid {
        display: grid;
        grid-template-columns:
            repeat(4, 1fr);

        gap: 12px;
        margin-bottom: 28px;
    }

    .agent-card {
        background: rgba(16, 21, 30, 0.88);
        border: 1px solid #202b3b;
        border-radius: 16px;
        padding: 17px;
        min-height: 112px;

        transition: all 0.2s ease;
    }

    .agent-card.active {
        border-color: #35d9ff;
        box-shadow:
            0 0 25px rgba(53, 217, 255, 0.12);
    }

    .agent-card.complete {
        border-color: #38d39f;
    }

    .agent-number {
        color: #647287;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    .agent-name {
        color: #edf2f8;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .agent-status {
        color: #7f8b9c;
        font-size: 12px;
    }

    .agent-card.active .agent-status {
        color: #35d9ff;
    }

    .agent-card.complete .agent-status {
        color: #38d39f;
    }

    /* Result card */
    .result-container {
        margin-top: 35px;
        background: rgba(14, 19, 28, 0.92);
        border: 1px solid #222e3e;
        border-radius: 20px;
        padding: 30px;
    }

    .result-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .result-title {
        font-size: 22px;
        font-weight: 750;
    }

    .result-badge {
        font-size: 11px;
        font-weight: 700;
        padding: 6px 11px;
        border-radius: 20px;

        color: #38d39f;
        background: rgba(56, 211, 159, 0.10);
        border: 1px solid rgba(56, 211, 159, 0.22);
    }

    /* Markdown */
    .stMarkdown {
        color: #dce3ed;
    }

    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3 {
        color: #f3f7fb;
    }

    .stMarkdown h1 {
        font-size: 30px;
    }

    .stMarkdown h2 {
        font-size: 21px;
        margin-top: 25px;
    }

    .stMarkdown p,
    .stMarkdown li {
        line-height: 1.75;
        color: #c2ccd8;
    }

    /* Mobile */
    @media (max-width: 800px) {

        .hero-title {
            font-size: 34px;
        }

        .agent-grid {
            grid-template-columns:
                repeat(2, 1fr);
        }
    }

    @media (max-width: 500px) {

        .agent-grid {
            grid-template-columns: 1fr;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# UI HELPERS
# ---------------------------------------------------------

def render_brand():
    st.markdown(
        """
        <div class="brand">

            <div class="brand-icon">
                ✦
            </div>

            <div>
                <div class="brand-title">
                    Research AI
                </div>

                <div class="brand-subtitle">
                    Multi-agent research assistant
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agents():

    cards = ""

    for index, agent_name in enumerate(AGENTS):

        state = st.session_state.agent_states.get(
            agent_name,
            "waiting",
        )

        if state == "active":
            status = "Working..."
            card_class = "active"

        elif state == "complete":
            status = "Completed"
            card_class = "complete"

        else:
            status = "Waiting"
            card_class = ""

        cards += f"""
        <div class="agent-card {card_class}">

            <div class="agent-number">
                STEP {index + 1}
            </div>

            <div class="agent-name">
                {agent_name}
            </div>

            <div class="agent-status">
                {status}
            </div>

        </div>
        """

    st.markdown(
        f"""
        <div class="agent-grid">
            {cards}
        </div>
        """,
        unsafe_allow_html=True,
    )


def clean_result(result):

    if result is None:
        return ""

    if hasattr(result, "raw"):
        text = result.raw
    else:
        text = str(result)

    if not isinstance(text, str):
        text = str(text)

    # Remove accidental Python-style object representations.
    text = re.sub(
        r"<(?:class|function|module)[^>]*>",
        "",
        text,
    )

    # Remove common internal execution labels.
    text = re.sub(
        r"(?i)(agent execution|agent output|task output):",
        "",
        text,
    )

    return text.strip()


def update_agent_status(agent):

    agent_text = ""

    if hasattr(agent, "role"):
        agent_text = str(agent.role)

    elif hasattr(agent, "agent"):
        internal_agent = getattr(agent, "agent", None)

        if hasattr(internal_agent, "role"):
            agent_text = str(internal_agent.role)

    else:
        agent_text = str(agent)

    agent_text = agent_text.lower()

    matched_agent = None

    if "research" in agent_text:
        matched_agent = "Researcher"

    elif "fact" in agent_text or "verification" in agent_text:
        matched_agent = "Fact Checker"

    elif "analyst" in agent_text or "analysis" in agent_text:
        matched_agent = "Analyst"

    elif "writer" in agent_text or "writing" in agent_text:
        matched_agent = "Writer"

    if matched_agent is None:
        return

    st.session_state.current_agent = matched_agent

    current_index = AGENTS.index(matched_agent)

    for index, name in enumerate(AGENTS):

        if index < current_index:
            st.session_state.agent_states[name] = "complete"

        elif index == current_index:
            st.session_state.agent_states[name] = "active"

        else:
            st.session_state.agent_states[name] = "waiting"


# ---------------------------------------------------------
# BRAND
# ---------------------------------------------------------

render_brand()


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            Research anything with a
            <span>team of AI agents.</span>
        </div>

        <div class="hero-text">
            Ask a research question and let four specialized AI agents
            search, verify, analyze, and write a clear research report.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# QUESTION INPUT
# ---------------------------------------------------------

st.markdown(
    '<div class="input-label">What would you like to research?</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "",
    height=125,
    placeholder=(
        "Example: What are the latest applications of generative AI "
        "in healthcare?"
    ),
    label_visibility="collapsed",
)


# ---------------------------------------------------------
# BUTTON
# ---------------------------------------------------------

run_research = st.button(
    "✦  Start Research",
    use_container_width=True,
)


# ---------------------------------------------------------
# WORKFLOW TITLE
# ---------------------------------------------------------

st.markdown(
    '<div class="workflow-title">Research workflow</div>',
    unsafe_allow_html=True,
)

render_agents()


# ---------------------------------------------------------
# RUN RESEARCH
# ---------------------------------------------------------

if run_research:

    if not question.strip():

        st.warning(
            "Please enter a research question first."
        )

        st.stop()

    # Reset states
    st.session_state.current_agent = "Researcher"

    st.session_state.agent_states = {
        "Researcher": "active",
        "Fact Checker": "waiting",
        "Analyst": "waiting",
        "Writer": "waiting",
    }

    st.session_state.research_result = None

    # Refresh workflow
    render_agents()

    try:

        with st.spinner("Your research team is working..."):

            crew = build_crew(
                status_callback=update_agent_status
            )

            result = crew.kickoff(
                inputs={
                    "question": question.strip()
                }
            )

        # Mark all agents complete
        st.session_state.agent_states = {
            "Researcher": "complete",
            "Fact Checker": "complete",
            "Analyst": "complete",
            "Writer": "complete",
        }

        st.session_state.current_agent = None

        st.session_state.research_result = clean_result(
            result
        )

    except Exception:

        st.session_state.agent_states = {
            "Researcher": "waiting",
            "Fact Checker": "waiting",
            "Analyst": "waiting",
            "Writer": "waiting",
        }

        st.session_state.current_agent = None

        st.error(
            "The research could not be completed right now. "
            "Please wait a little and try again."
        )

        st.stop()


# ---------------------------------------------------------
# SHOW UPDATED WORKFLOW
# ---------------------------------------------------------

if st.session_state.research_result:

    render_agents()

    st.markdown(
        """
        <div class="result-container">

            <div class="result-header">

                <div class="result-title">
                    Research Report
                </div>

                <div class="result-badge">
                    RESEARCH COMPLETE
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        st.session_state.research_result
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:60px;
        color:#566274;
        font-size:12px;
    ">
        Research AI · Powered by a multi-agent research workflow
    </div>
    """,
    unsafe_allow_html=True,
)
