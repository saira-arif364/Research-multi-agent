import streamlit as st
import traceback

from crew import build_crew


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Research AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(56, 189, 248, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            #07111f;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

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
        font-size: 24px;
        background:
            linear-gradient(
                135deg,
                #38bdf8,
                #6366f1
            );
        box-shadow:
            0 0 30px
            rgba(56, 189, 248, 0.25);
    }

    .brand-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .brand-subtitle {
        color: #8fa3ba;
        font-size: 14px;
        margin-top: 2px;
    }

    .hero {
        padding: 38px;
        margin-top: 24px;
        margin-bottom: 24px;
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                rgba(15, 31, 51, 0.97),
                rgba(9, 22, 39, 0.97)
            );
        border:
            1px solid
            rgba(148, 163, 184, 0.12);
        box-shadow:
            0 20px 70px
            rgba(0, 0, 0, 0.25);
    }

    .hero-title {
        font-size: 42px;
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -1.8px;
        margin-bottom: 14px;
    }

    .gradient-text {
        background:
            linear-gradient(
                90deg,
                #67e8f9,
                #60a5fa,
                #a78bfa
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #9fb1c5;
        font-size: 16px;
        line-height: 1.7;
        max-width: 760px;
    }

    .pipeline {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 22px 0;
    }

    .pipeline-step {
        flex: 1;
        padding: 13px 10px;
        text-align: center;
        border-radius: 14px;
        background:
            rgba(12, 28, 47, 0.75);
        border:
            1px solid
            rgba(148, 163, 184, 0.09);
        color: #71869d;
        font-size: 12px;
        font-weight: 650;
    }

    .pipeline-arrow {
        color: #475569;
    }

    .agent-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 11px 0;
        border-bottom:
            1px solid
            rgba(148, 163, 184, 0.07);
    }

    .agent-row:last-child {
        border-bottom: none;
    }

    .agent-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .dot-active {
        background: #38bdf8;
        box-shadow:
            0 0 14px
            rgba(56, 189, 248, 0.9);
    }

    .dot-complete {
        background: #34d399;
    }

    .dot-waiting {
        background: #475569;
    }

    .agent-name {
        font-weight: 650;
        color: #e5edf7;
    }

    .agent-status {
        margin-left: auto;
        color: #71869d;
        font-size: 12px;
    }

    .current-agent {
        padding: 22px;
        border-radius: 20px;
        margin-bottom: 20px;
        background:
            linear-gradient(
                135deg,
                rgba(14, 165, 233, 0.10),
                rgba(99, 102, 241, 0.10)
            );
        border:
            1px solid
            rgba(56, 189, 248, 0.18);
        box-shadow:
            0 12px 40px
            rgba(0, 0, 0, 0.12);
    }

    .current-label {
        font-size: 11px;
        color: #67e8f9;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .current-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .current-description {
        color: #8fa3ba;
        font-size: 13px;
    }

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 13px 20px;
        font-weight: 750;
        color: white;
        background:
            linear-gradient(
                135deg,
                #0ea5e9,
                #6366f1
            );
        box-shadow:
            0 12px 28px
            rgba(37, 99, 235, 0.22);
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 16px 34px
            rgba(37, 99, 235, 0.30);
    }

    textarea {
        border-radius: 16px !important;
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 28px 0 15px;
    }

    .result-title {
        font-size: 26px;
        font-weight: 800;
    }

    .source-badge {
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 12px;
        color: #bae6fd;
        background:
            rgba(14, 165, 233, 0.10);
        border:
            1px solid
            rgba(56, 189, 248, 0.16);
    }

    section[data-testid="stSidebar"] {
        background: #081522;
        border-right:
            1px solid
            rgba(148, 163, 184, 0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# AGENTS
# =========================================================

AGENTS = [
    "Researcher",
    "Fact Checker",
    "Analyst",
    "Writer",
]


# =========================================================
# SESSION STATE
# =========================================================

if "agent_states" not in st.session_state:
    st.session_state.agent_states = {
        agent: "waiting"
        for agent in AGENTS
    }


if "current_agent" not in st.session_state:
    st.session_state.current_agent = None


# =========================================================
# SAFE AGENT CALLBACK
# =========================================================

def research_status_callback(agent):
    """
    CrewAI may send either an agent name or an Agent object.
    This function safely handles both.
    """

    # Try to get the agent's role
    agent_name = getattr(agent, "role", None)

    # If there is no role, convert the object to text
    if not agent_name:
        agent_name = str(agent)

    # Find the closest known agent
    matched_agent = None

    for known_agent in AGENTS:
        if known_agent.lower() in agent_name.lower():
            matched_agent = known_agent
            break

    # If the agent cannot be matched, don't crash the whole app
    if matched_agent is None:
        return

    st.session_state.current_agent = matched_agent

    current_index = AGENTS.index(matched_agent)

    for index, agent_name in enumerate(AGENTS):

        if index < current_index:
            st.session_state.agent_states[agent_name] = "complete"

        elif index == current_index:
            st.session_state.agent_states[agent_name] = "active"

        else:
            st.session_state.agent_states[agent_name] = "waiting"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:20px;
            font-weight:800;
            margin-bottom:6px;
        ">
            🔬 Research AI
        </div>

        <div style="
            color:#8195aa;
            font-size:13px;
            line-height:1.6;
            margin-bottom:24px;
        ">
            A multi-agent research workspace powered by
            CrewAI and Groq.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Research Pipeline")

    for agent in AGENTS:

        state = st.session_state.agent_states[agent]

        if state == "active":
            dot_class = "dot-active"
            status = "Working"

        elif state == "complete":
            dot_class = "dot-complete"
            status = "Complete"

        else:
            dot_class = "dot-waiting"
            status = "Waiting"

        st.markdown(
            f"""
            <div class="agent-row">

                <div class="agent-dot {dot_class}"></div>

                <div class="agent-name">
                    {agent}
                </div>

                <div class="agent-status">
                    {status}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.caption("LLM: Groq GPT-OSS 120B")
    st.caption("Framework: CrewAI")
    st.caption("Search: Tavily")


# =========================================================
# BRAND
# =========================================================

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
                Multi-agent research workspace
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">

            Turn a question into

            <span class="gradient-text">
                evidence.
            </span>

        </div>

        <div class="hero-description">

            Four specialized AI agents research,
            verify, analyze and write a professional
            research report.

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PIPELINE
# =========================================================

st.markdown(
    """
    <div class="pipeline">

        <div class="pipeline-step">
            🔎 Research
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            ✓ Verify
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            🧠 Analyze
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            ✍️ Write
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# QUESTION INPUT
# =========================================================

question = st.text_area(
    "Research question",

    placeholder=(
        "Ask anything you want the research team to investigate...\n\n"
        "Example: What are the latest developments in AI agents in 2026?"
    ),

    height=135,

    label_visibility="collapsed",
)


# =========================================================
# START BUTTON
# =========================================================

start = st.button(
    "🚀 Start Research",
    type="primary",
)


# =========================================================
# EXECUTE RESEARCH
# =========================================================

if start:

    if not question.strip():

        st.warning(
            "Please enter a research question first."
        )

        st.stop()


    # -----------------------------------------------------
    # Reset agent status
    # -----------------------------------------------------

    st.session_state.agent_states = {
        agent: "waiting"
        for agent in AGENTS
    }

    st.session_state.current_agent = None


    # -----------------------------------------------------
    # Current agent placeholder
    # -----------------------------------------------------

    current_placeholder = st.empty()


    current_placeholder.markdown(
        """
        <div class="current-agent">

            <div class="current-label">
                Research Team
            </div>

            <div class="current-title">
                🟡 Preparing agents...
            </div>

            <div class="current-description">
                Initializing the research workflow.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # Run research
    # -----------------------------------------------------

    try:

        crew = build_crew(
            status_callback=research_status_callback
        )


        result = crew.kickoff(
            inputs={
                "question": question.strip()
            }
        )


        # -------------------------------------------------
        # Mark all agents complete
        # -------------------------------------------------

        for agent in AGENTS:
            st.session_state.agent_states[agent] = "complete"

        st.session_state.current_agent = None


        # -------------------------------------------------
        # Completion message
        # -------------------------------------------------

        current_placeholder.markdown(
            """
            <div class="current-agent">

                <div class="current-label">
                    Research Complete
                </div>

                <div class="current-title">
                    🟢 Your report is ready
                </div>

                <div class="current-description">
                    The research team completed all four stages.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # -------------------------------------------------
        # Result header
        # -------------------------------------------------

        st.markdown(
            """
            <div class="result-header">

                <div class="result-title">
                    Research Report
                </div>

                <div class="source-badge">
                    ✓ Multi-agent research
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # -------------------------------------------------
        # Display result
        # -------------------------------------------------

        st.markdown(str(result))


    except Exception as error:

        # -----------------------------------------------
        # Reset active agent
        # -----------------------------------------------

        st.session_state.current_agent = None


        current_placeholder.markdown(
            """
            <div class="current-agent">

                <div class="current-label">
                    Research Error
                </div>

                <div class="current-title">
                    🔴 The research workflow failed
                </div>

                <div class="current-description">
                    See the technical details below.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # -----------------------------------------------
        # User-friendly error
        # -----------------------------------------------

        st.error(
            "The research team encountered an error."
        )


        # -----------------------------------------------
        # Show actual error
        # -----------------------------------------------

        with st.expander(
            "🔧 Technical error details",
            expanded=True,
        ):

            st.error(str(error))

            st.code(
                traceback.format_exc(),
                language="text",
            )
