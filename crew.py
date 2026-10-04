import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

import os

from crewai import Crew, LLM, Process, Task
from crewai_tools import TavilySearchTool, ScrapeWebsiteTool

from researcher import create_researcher
from fact_checker import create_fact_checker
from analyst import create_analyst
from writer import create_writer


MODEL_NAME = "groq/openai/gpt-oss-120b"


def build_crew(status_callback=None):

    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Streamlit Secrets."
        )

    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError(
            "TAVILY_API_KEY is missing. Add it in Streamlit Secrets."
        )

    llm = LLM(
        model=MODEL_NAME,
        temperature=0.2,
        max_completion_tokens=4096,
    )

    search_tool = TavilySearchTool()
    scrape_tool = ScrapeWebsiteTool()

    research_tools = [
        search_tool,
        scrape_tool,
    ]

    researcher = create_researcher(
        llm=llm,
        tools=research_tools,
        step_callback=status_callback,
    )

    fact_checker = create_fact_checker(
        llm=llm,
        tools=research_tools,
        step_callback=status_callback,
    )

    analyst = create_analyst(
        llm=llm,
        step_callback=status_callback,
    )

    writer = create_writer(
        llm=llm,
        step_callback=status_callback,
    )

    research_task = Task(
        description="""
        Research the following question:

        {question}

        Find accurate and recent information from reliable
        web sources.

        Prefer primary sources, official documentation,
        academic research, reputable organizations, and
        high-quality journalism.

        Collect important facts, dates, numbers, evidence,
        source names, and source URLs.

        Identify conflicting or uncertain information.

        Do not invent facts or sources.
        """,
        expected_output="""
        Detailed research notes containing:

        - Key findings
        - Important facts
        - Dates
        - Numbers
        - Evidence
        - Source names
        - Source URLs
        - Conflicting or uncertain information
        """,
        agent=researcher,
    )

    fact_check_task = Task(
        description="""
        Fact-check the research produced by the researcher.

        Research question:

        {question}

        Independently verify important claims using web
        search and scraping tools.

        Pay special attention to:

        - Numbers
        - Dates
        - Recent developments
        - Important claims
        - Unsupported statements
        - Contradictory information
        - Outdated information
        - Source quality

        Classify claims as:

        VERIFIED
        PARTIALLY VERIFIED
        CONTRADICTED
        UNSUPPORTED
        OUTDATED

        Explain the evidence behind each assessment.
        """,
        expected_output="""
        A structured fact-checking report containing:

        - Claim
        - Verification status
        - Evidence
        - Source
        - URL
        - Important uncertainty
        """,
        agent=fact_checker,
        context=[
            research_task,
        ],
    )

    analysis_task = Task(
        description="""
        Analyze the research and fact-checking results.

        Research question:

        {question}

        Focus on verified information.

        Identify:

        - Main findings
        - Important comparisons
        - Patterns and trends
        - Conflicting evidence
        - Limitations
        - Research gaps

        Do not treat unsupported claims as facts.
        Do not invent missing information.
        """,
        expected_output="""
        A structured analytical brief containing:

        1. Main findings
        2. Supporting evidence
        3. Important comparisons
        4. Conflicting evidence
        5. Limitations
        6. Research gaps
        7. Important points for the final report
        """,
        agent=analyst,
        context=[
            research_task,
            fact_check_task,
        ],
    )

    writing_task = Task(
        description="""
        Write the final research report.

        Research question:

        {question}

        Use the research, fact-checking, and analysis
        produced by the previous agents.

        Create a professional Markdown report.

        Structure:

        # Research Title

        ## Executive Summary

        ## Key Findings

        ## Detailed Analysis

        ## Evidence and Sources

        ## Limitations

        ## Conclusion

        ## Sources

        Requirements:

        - Be factual.
        - Be clear.
        - Be balanced.
        - Preserve uncertainty.
        - Do not fabricate information.
        - Do not fabricate citations.
        - Do not fabricate URLs.
        - Do not invent quotations.
        - Use Markdown formatting.
        - Include source URLs when available.
        """,
        expected_output="""
        A polished Markdown research report ready to
        display in the Streamlit application.
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
