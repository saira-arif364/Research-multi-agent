import re
import streamlit as st

from crew import build_crew


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Research AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

AGENTS = [
    "Researcher",
    "Fact Checker",
    "Analyst",
    "Writer",
]

if "agent_states" not in st.session_state:
    st.session_state.agent_states = {
        "Researcher": "waiting",
        "Fact Checker": "waiting",
        "Analyst": "waiting",
        "Writer": "waiting",
    }

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(53, 217, 255, 0.09),
                transparent 28%
            ),
            radial-gradient(
                circle at 92% 12%,
                rgba(113, 101, 255, 0.09),
                transparent 30%
            ),
            #080b12;

        color: #f4f7fb;
    }

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.8rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       BRAND
       ===================================================== */

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 10px;
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
            #7165ff
        );

        color: white;
        font-size: 25px;
        font-weight: 800;

        box-shadow:
            0 0 32px rgba(53, 217, 255, 0.20);
    }

    .brand-title {
        font-size: 30px;
        font-weight: 780;
        letter-spacing: -0.7px;
        color: #f4f7fb;
    }

    .brand-subtitle {
        font-size: 13px;
        color: #7f8b9d;
        margin-top: 2px;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        margin-top: 48px;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 46px;
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: -1.8px;
        color: #f4f7fb;
        margin-bottom: 15px;
    }

    .hero-gradient {
        background: linear-gradient(
            90deg,
            #35d9ff,
            #8b7cff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 730px;
        color: #96a2b4;
        font-size: 17px;
        line-height: 1.65;
    }


    /* =====================================================
       QUESTION AREA
       ===================================================== */

    .question-label {
        color: #dce4ee;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    textarea {
        background: #10151e !important;
        color: #f4f7fb !important;

        border: 1px solid #263142 !important;
        border-radius: 15px !important;

        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    textarea:focus {
        border-color: #35d9ff !important;
        box-shadow:
            0 0 0 1px rgba(53, 217, 255, 0.35) !important;
    }


    /* =====================================================
       BUTTON
       ===================================================== */

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
        font-weight: 750;

        box-shadow:
            0 8px 28px rgba(52, 167, 255, 0.17);

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 12px 36px rgba(52, 167, 255, 0.28);
    }


    /* =====================================================
       WORKFLOW
       ===================================================== */

    .workflow-heading {
        margin-top: 42px;
        margin-bottom: 15px;

        font-size: 18px;
        font-weight: 750;
        color: #edf2f8;
    }

    .agent-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }

    .agent-card {
        min-height: 112px;

        padding: 17px;

        border-radius: 16px;

        background: rgba(16, 21, 30, 0.88);

        border: 1px solid #202b3b;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .agent-card.active {
        border-color: #35d9ff;

        box-shadow:
            0 0 26px rgba(53, 217, 255, 0.13);
    }

    .agent-card.complete {
        border-color: #38d39f;

        box-shadow:
            0 0 20px rgba(56, 211, 159, 0.07);
    }

    .agent-step {
        color: #5f6d81;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
    }

    .agent-name {
        color: #edf2f8;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .agent-status {
        color: #758296;
        font-size: 12px;
    }

    .agent-card.active .agent-status {
        color: #35d9ff;
    }

    .agent-card.complete .agent-status {
        color: #38d39f;
    }


    /* =====================================================
       RESULT
       ===================================================== */

    .result-header {
        margin-top: 38px;
        margin-bottom: 18px;

        padding: 18px 20px;

        border-radius: 16px;

        background: rgba(14, 19, 28, 0.92);

        border: 1px solid #222e3e;

        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .result-title {
        color: #f3f7fb;
        font-size: 21px;
        font-weight: 760;
    }

    .result-badge {
        color: #38d39f;

        background: rgba(
            56,
            211,
            159,
            0.10
        );

        border: 1px solid rgba(
            56,
            211,
            159,
            0.22
        );

        padding: 6px 11px;

        border-radius: 20px;

        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }


    /* =====================================================
       REPORT
       ===================================================== */

    .report-box {
        background: rgba(14, 19, 28, 0.80);

        border: 1px solid #222e3e;

        border-radius: 18px;

        padding: 28px;
    }

    .stMarkdown {
        color: #c4ceda;
    }

    .stMarkdown h1 {
        color: #f4f7fb;
        font-size: 30px;
        font-weight: 780;
    }

    .stMarkdown h2 {
        color: #eaf0f7;
        font-size: 21px;
        margin-top: 28px;
    }

    .stMarkdown h3 {
        color: #eaf0f7;
    }

    .stMarkdown p {
        color: #c2ccd8;
        line-height: 1.75;
    }

    .stMarkdown li {
        color: #c2ccd8;
        line-height: 1.7;
    }

    .stMarkdown a {
        color: #35d9ff;
    }


    /* =====================================================
       ERROR
       ===================================================== */

    .error-note {
        margin-top: 20px;

        padding: 15px 17px;

        border-radius: 13px;

        background: rgba(255, 100, 100, 0.06);

        border: 1px solid rgba(
            255,
            100,
            100,
            0.18
        );

        color: #d8a7a7;

        font-size: 13px;
        line-height: 1.6;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;

        margin-top: 60px;

        color: #4f5b6d;

        font-size: 12px;
    }


    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 850px) {

        .hero-title {
            font-size: 36px;
        }

        .agent-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 520px) {

        .hero-title {
            font-size: 31px;
        }

        .agent-grid {
            grid-template-columns: 1fr;
        }

        .result-header {
            align-items: flex-start;
            gap: 10px;
            flex-direction: column;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNCTIONS
# =========================================================

def reset_agents():
    st.session_state.agent_states = {
        "Researcher": "waiting",
        "Fact Checker": "waiting",
        "Analyst": "waiting",
        "Writer": "waiting",
    }


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


def render_workflow():

    cards = ""

    for index, agent in enumerate(AGENTS):

        state = st.session_state.agent_states.get(
            agent,
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

            <div class="agent-step">
                STEP {index + 1}
            </div>

            <div class="agent-name">
                {agent}
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


def update_agent_status(agent):

    agent_name = ""

    if hasattr(agent, "role"):
        agent_name = str(agent.role)

    elif hasattr(agent, "agent"):

        internal_agent = getattr(
            agent,
            "agent",
            None,
        )

        if hasattr(internal_agent, "role"):
            agent_name = str(
                internal_agent.role
            )

    else:
        agent_name = str(agent)

    agent_name = agent_name.lower()

    matched = None

    if "research" in agent_name:
        matched = "Researcher"

    elif (
        "fact" in agent_name
        or "verification" in agent_name
    ):
        matched = "Fact Checker"

    elif (
        "analyst" in agent_name
        or "analysis" in agent_name
    ):
        matched = "Analyst"

    elif (
        "writer" in agent_name
        or "writing" in agent_name
    ):
        matched = "Writer"

    if matched is None:
        return

    current_index = AGENTS.index(matched)

    for index, name in enumerate(AGENTS):

        if index < current_index:
            st.session_state.agent_states[name] = "complete"

        elif index == current_index:
            st.session_state.agent_states[name] = "active"

        else:
            st.session_state.agent_states[name] = "waiting"


def clean_result(result):

    if result is None:
        return ""

    if hasattr(result, "raw"):
        text = result.raw
    else:
        text = str(result)

    if not isinstance(text, str):
        text = str(text)

    # Remove common internal execution labels.
    text = re.sub(
        r"(?i)(agent execution|agent output|task output):",
        "",
        text,
    )

    return text.strip()


# =========================================================
# BRAND
# =========================================================

render_brand()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            Research anything with a
            <span class="hero-gradient">
                team of AI agents.
            </span>
        </div>

        <div class="hero-description">
            Ask a research question and let specialized AI agents
            research, verify, analyze, and write a clear report.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# QUESTION
# =========================================================

st.markdown(
    """
    <div class="question-label">
        What would you like to research?
    </div>
    """,
    unsafe_allow_html=True,
)

question = st.text_area(
    "Research question",
    height=125,
    placeholder=(
        "Example: What are the latest applications "
        "of generative AI in healthcare?"
    ),
    label_visibility="collapsed",
)


# =========================================================
# START BUTTON
# =========================================================

run_research = st.button(
    "✦  Start Research",
    use_container_width=True,
)


# =========================================================
# WORKFLOW
# =========================================================

st.markdown(
    """
    <div class="workflow-heading">
        Research workflow
    </div>
    """,
    unsafe_allow_html=True,
)

render_workflow()


# =========================================================
# EXECUTION
# =========================================================

if run_research:

    if not question.strip():

        st.warning(
            "Please enter a research question first."
        )

        st.stop()

    # Clear old result.
    st.session_state.research_result = None

    st.session_state.last_question = question.strip()

    reset_agents()

    # Researcher starts.
    st.session_state.agent_states[
        "Researcher"
    ] = "active"

    render_workflow()

    try:

        with st.spinner(
            "Your research team is working..."
        ):

            crew = build_crew(
                status_callback=update_agent_status
            )

            result = crew.kickoff(
                inputs={
                    "question": question.strip()
                }
            )

        # All agents completed.
        st.session_state.agent_states = {
            "Researcher": "complete",
            "Fact Checker": "complete",
            "Analyst": "complete",
            "Writer": "complete",
        }

        st.session_state.research_result = clean_result(
            result
        )

    except Exception as e:

        reset_agents()

        st.error(
            "Research could not be completed right now. "
            "Please try again in a moment."
        )

        # Keep technical information hidden
        # unless the user explicitly opens it.
        with st.expander(
            "Technical details"
        ):
            st.code(
                str(e),
                language="text",
            )

        st.stop()


# =========================================================
# FINAL RESULT
# =========================================================

if st.session_state.research_result:

    render_workflow()

    st.markdown(
        """
        <div class="result-header">

            <div class="result-title">
                Research Report
            </div>

            <div class="result-badge">
                RESEARCH COMPLETE
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="report-box">',
        unsafe_allow_html=True,
    )

    st.markdown(
        st.session_state.research_result
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Research AI · Multi-agent research workflow
    </div>
    """,
    unsafe_allow_html=True,
)
