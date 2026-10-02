from __future__ import annotations

import streamlit as st

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

    /* ---------- Global ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(56, 189, 248, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            #07111f;
        color: #e5edf7;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- Header ---------- */

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
        background: linear-gradient(
            135deg,
            #38bdf8,
            #6366f1
        );
        box-shadow:
            0 0 30px rgba(56, 189, 248, 0.22);
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

    /* ---------- Hero ---------- */

    .hero {
        padding: 36px 38px;
        margin-top: 24px;
        margin-bottom: 22px;
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                rgba(15, 31, 51, 0.96),
                rgba(9, 22, 39, 0.96)
            );
        border: 1px solid rgba(148, 163, 184, 0.12);
        box-shadow:
            0 20px 70px rgba(0, 0, 0, 0.22);
    }

    .hero-title {
        font-size: 42px;
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -1.8px;
        margin-bottom: 14px;
    }

    .gradient-text {
        background: linear-gradient(
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

    /* ---------- Agent cards ---------- */

    .agent-panel {
        padding: 20px;
        border-radius: 20px;
        background: rgba(12, 28, 47, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.10);
        margin-bottom: 20px;
    }

    .agent-title {
        font-size: 13px;
        font-weight: 700;
        color: #8fa3ba;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 14px;
    }

    .agent-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 11px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.07);
    }

    .agent-row:last-child {
        border-bottom: none;
    }

    .agent-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .active {
        background: #38bdf8;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.9);
    }

    .complete {
        background: #34d399;
    }

    .waiting {
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

    /* ---------- Buttons ---------- */

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 12px 20px;
        font-weight: 750;
        color: white;
        background: linear-gradient(
            135deg,
            #0ea5e9,
            #6366f1
        );
        box-shadow:
            0 12px 28px rgba(37, 99, 235, 0.22);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 16px 34px rgba(37, 99, 235, 0.30);
    }

    /* ---------- Text area ---------- */

    textarea {
        border-radius: 16px !important;
    }

    /* ---------- Result ---------- */

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 25px 0 12px;
    }

    .result-title {
        font-size: 25px;
        font-weight: 800;
    }

    .source-badge {
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 12px;
        color: #bae6fd;
        background: rgba(14, 165, 233, 0.10);
        border: 1px solid rgba(56, 189, 248, 0.16);
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #081522;
        border-right: 1px solid rgba(148, 163, 184, 0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
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
        name: "waiting"
        for name in AGENTS
    }

if "current_agent" not in st.session_state:
    st.session_state.current_agent = None


# =========================================================
# CALLBACK
# =========================================================

def make_step_callback(agent_name, status_placeholder):

    def callback(step_output):

        st.session_state.current_agent = agent_name

        for name in AGENTS:

            if AGENTS.index(name) < AGENTS.index(agent_name):
                st.session_state.agent_states[name] = "complete"

            elif name == agent_name:
                st.session_state.agent_states[name] = "active"

        status_placeholder.markdown(
            f"""
            <div class="agent-panel">

                <div class="agent-title">
                    Live Research Team
                </div>

                <div style="
                    font-size:22px;
                    font-weight:800;
                    margin-bottom:6px;
                ">
                    🔵 {agent_name} is working
                </div>

                <div style="
                    color:#8fa3ba;
                    font-size:14px;
                ">
                    The team is processing your research question...
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    return callback


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
            icon = "🔵"
            label = "Working"

        elif state == "complete":
            icon = "🟢"
            label = "Complete"

        else:
            icon = "⚪"
            label = "Waiting"

        st.markdown(
            f"""
            <div class="agent-row">

                <div>{icon}</div>

                <div class="agent-name">
                    {agent}
                </div>

                <div class="agent-status">
                    {label}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.caption(
        "LLM: Groq • Model: GPT-OSS 120B"
    )

    st.caption(
        "Orchestration: CrewAI"
    )


# =========================================================
# HEADER
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
            Four specialized AI agents research, verify, analyze,
            and write a professional report — with live visibility
            into who is working.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INPUT
# =========================================================

question = st.text_area(
    "Research question",
    placeholder=(
        "Example: What are the latest developments in "
        "generative AI agents in 2026?"
    ),
    height=120,
    label_visibility="collapsed",
)


col1, col2, col3 = st.columns([1, 1, 2])

with col1:

    start = st.button(
        "🚀 Start Research",
        type="primary",
    )

with col3:

    st.markdown(
        """
        <div style="
            color:#71869d;
            font-size:12px;
            padding-top:10px;
        ">
            The team will search, verify, analyze and write.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# RESEARCH EXECUTION
# =========================================================

if start:

    if not question.strip():

        st.warning(
            "Please enter a research question first."
        )

        st.stop()

    # Reset agent states
    st.session_state.agent_states = {
        name: "waiting"
        for name in AGENTS
    }

    st.session_state.current_agent = None

    status_placeholder = st.empty()

    status_placeholder.markdown(
        """
        <div class="agent-panel">

            <div class="agent-title">
                Live Research Team
            </div>

            <div style="
                font-size:22px;
                font-weight:800;
                margin-bottom:6px;
            ">
                🟡 Preparing the research team...
            </div>

            <div style="
                color:#8fa3ba;
                font-size:14px;
            ">
                Initializing the agents and research tools.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    try:

        # The callback identifies which agent is currently active.
        callback = make_step_callback(
            "Researcher",
            status_placeholder,
        )

        crew = build_crew(
            step_callback=callback,
        )

        result = crew.kickoff(
            inputs={
                "question": question.strip()
            }
        )

        # Mark all agents complete.
        for name in AGENTS:
            st.session_state.agent_states[name] = "complete"

        status_placeholder.markdown(
            """
            <div class="agent-panel">

                <div class="agent-title">
                    Research Complete
                </div>

                <div style="
                    font-size:22px;
                    font-weight:800;
                    margin-bottom:6px;
                ">
                    🟢 Research team finished
                </div>

                <div style="
                    color:#8fa3ba;
                    font-size:14px;
                ">
                    Your report is ready below.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="result-header">

                <div class="result-title">
                    Research Report
                </div>

                <div class="source-badge">
                    ✓ Multi-agent verified
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(str(result))

    except Exception as exc:

        st.error(
            "The research team encountered an error."
        )

        with st.expander("Technical details"):

            st.code(
                str(exc)
            )
