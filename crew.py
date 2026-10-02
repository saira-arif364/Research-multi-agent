from __future__ import annotations

import os

from crewai import Agent, Crew, LLM, Process, Task

from researcher import create_researcher
from fact_checker import create_fact_checker
from analyst import create_analyst
from writer import create_writer


MODEL_NAME = "groq/openai/gpt-oss-120b"


def build_crew(step_callback=None):

    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to Streamlit Secrets."
        )

    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError(
            "TAVILY_API_KEY is missing. Add it to Streamlit Secrets."
        )

    llm = LLM(
        model=MODEL_NAME,
        temperature=0.2,
        max_completion_tokens=4096,
    )

    researcher = create_researcher(
        llm=llm,
        step_callback=step_callback,
    )

    fact_checker = create_fact_checker(
        llm=llm,
        step_callback=step_callback,
    )

    analyst = create_analyst(
        llm=llm,
        step_callback=step_callback,
    )

    writer = create_writer(
        llm=llm,
        step_callback=step_callback,
    )

    # -----------------------------------------------------
    # TASK 1 — Research
    # -----------------------------------------------------

    research_task = Task(
        description="""
        Research the following question:

        {question}

        Search the web extensively.

        Requirements:
        - Find recent information when relevant.
        - Prefer primary and authoritative sources.
        - Include useful secondary sources when appropriate.
        - Extract concrete facts, dates, numbers, and evidence.
        - Record source names and URLs.
        - Do not invent information.
        - Clearly identify uncertain or conflicting information.

        Produce detailed research notes for the fact checker.
        """,

        expected_output="""
        A detailed evidence collection containing:
        1. Key findings
        2. Important facts
        3. Relevant dates
        4. Important numbers
        5. Source names
        6. Source URLs
        7. Areas of uncertainty or disagreement
        """,

        agent=researcher,
    )

    # -----------------------------------------------------
    # TASK 2 — Fact Checking
    # -----------------------------------------------------

    fact_check_task = Task(
        description="""
        Carefully fact-check the research produced for:

        {question}

        Independently verify important claims using your web-search
        and web-scraping tools.

        Pay particular attention to:
        - numerical claims
        - dates
        - recent developments
        - claims that appear unsupported
        - contradictory sources
        - source quality
        - outdated information

        Do not simply agree with the researcher.

        Mark findings as:
        - VERIFIED
        - PARTIALLY VERIFIED
        - CONTRADICTED
        - UNSUPPORTED
        - OUTDATED

        Explain the evidence for important judgments.
        """,

        expected_output="""
        A structured fact-check report containing:
        - claim
        - verification status
        - evidence
        - source
        - URL
        - uncertainty or disagreement
        """,

        agent=fact_checker,

        context=[
            research_task,
        ],
    )

    # -----------------------------------------------------
    # TASK 3 — Analysis
    # -----------------------------------------------------

    analysis_task = Task(
        description="""
        Analyze the research and fact-checking results for:

        {question}

        Create an evidence-based analytical framework.

        Requirements:
        - Use verified information.
        - Do not treat unsupported claims as facts.
        - Reconcile conflicting evidence.
        - Identify the strongest findings.
        - Identify important limitations.
        - Calculate or verify numerical relationships when useful.
        - Do not invent missing evidence.

        This is analysis, not the final report.
        """,

        expected_output="""
        A structured analytical brief containing:
        1. Main findings
        2. Evidence supporting each finding
        3. Important comparisons
        4. Conflicting evidence
        5. Limitations
        6. Research gaps
        7. Key points the final writer should communicate
        """,

        agent=analyst,

        context=[
            research_task,
            fact_check_task,
        ],
    )

    # -----------------------------------------------------
    # TASK 4 — Final Report
    # -----------------------------------------------------

    writing_task = Task(
        description="""
        Write the final research report for:

        {question}

        Use the research, fact-checking, and analytical outputs provided
        by the previous agents.

        Before finalizing, use the Source Validator tool on important URLs
        when appropriate.

        The report should contain:

        # Title

        ## Executive Summary

        ## Key Findings

        ## Detailed Analysis

        ## Evidence and Sources

        ## Limitations

        ## Conclusion

        ### Sources

        Requirements:
        - Be factual and balanced.
        - Clearly distinguish evidence from interpretation.
        - Preserve important uncertainty.
        - Do not fabricate citations.
        - Do not invent URLs.
        - Do not invent quotations.
        - Do not make unsupported claims.
        - Use readable Markdown.
        - Cite sources using Markdown links when URLs are available.
        """,

        expected_output="""
        A polished Markdown research report ready to display in a
        professional research application.
        """,

        agent=writer,

        context=[
            research_task,
            fact_check_task,
            analysis_task,
        ],
    )

    crew = Crew(
        agents=[
            researcher,
            fact_checker,
            analyst,
            writer,
        ],

        tasks=[
            research_task,
            fact_check_task,
            analysis_task,
            writing_task,
        ],

        process=Process.sequential,

        verbose=False,
    )

    return crew
