
Those **must not be inside the Python file**. Also, everything inside `build_crew()` must be indented.

Replace your **entire `crew.py`** with the following. **Copy only the code inside the writing block, not the ``` markers.**

:::writing{variant="document" id="69427" title="Corrected crew.py"}
import os

from crewai import Crew, LLM, Process, Task
from crewai_tools import TavilySearchTool, ScrapeWebsiteTool

from researcher import create_researcher
from fact_checker import create_fact_checker
from analyst import create_analyst
from writer import create_writer


MODEL_NAME = "groq/openai/gpt-oss-120b"


def build_crew(status_callback=None):

    # Check API keys

    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Streamlit Secrets."
        )

    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError(
            "TAVILY_API_KEY is missing. Add it in Streamlit Secrets."
        )

    # Groq LLM

    llm = LLM(
        model=MODEL_NAME,
        temperature=0.2,
        max_completion_tokens=4096,
    )

    # Research tools

    search_tool = TavilySearchTool()
    scrape_tool = ScrapeWebsiteTool()

    research_tools = [
        search_tool,
        scrape_tool,
    ]

    # Agents

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

    # Task 1 — Research

    research_task = Task(
        description="""
        Research the following question:

        {question}

        Your job is to collect reliable evidence from the web.

        Requirements:

        1. Search for relevant information.
        2. Prefer recent information when the topic requires it.
        3. Prefer primary and authoritative sources.
        4. Use reputable secondary sources when useful.
        5. Collect important facts, dates and numbers.
        6. Record source names and URLs.
        7. Identify conflicting information.
        8. Do not invent facts or sources.

        Produce detailed research notes that another agent
        can fact-check.
        """,

        expected_output="""
        A detailed research package containing:

        - Key findings
        - Important facts
        - Dates
        - Numbers
        - Relevant evidence
        - Source names
        - Source URLs
        - Conflicting or uncertain information
        """,

        agent=researcher,
    )

    # Task 2 — Fact Check

    fact_check_task = Task(
        description="""
        Fact-check the research produced by the researcher.

        Research question:

        {question}

        Do NOT simply trust the researcher's information.

        Independently verify important claims using your
        web search and scraping tools.

        Pay special attention to:

        - Numbers
        - Dates
        - Recent developments
        - Important claims
        - Unsupported statements
        - Contradictory information
        - Outdated information
        - Source quality

        Classify important claims as:

        VERIFIED
        PARTIALLY VERIFIED
        CONTRADICTED
        UNSUPPORTED
        OUTDATED

        Explain the evidence behind your assessment.
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

    # Task 3 — Analysis

    analysis_task = Task(
        description="""
        Analyze the research and fact-checking results.

        Research question:

        {question}

        Use the evidence from the previous agents.

        Requirements:

        - Focus on verified information.
        - Do not treat unsupported claims as facts.
        - Identify the strongest findings.
        - Compare important evidence.
        - Identify patterns and trends.
        - Explain conflicting evidence.
        - Identify limitations.
        - Identify research gaps.
        - Do not invent missing information.

        Produce an analytical brief for the final writer.
        """,

        expected_output="""
        A structured analytical brief containing:

        1. Main findings
        2. Evidence supporting the findings
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

    # Task 4 — Writing

    writing_task = Task(
        description="""
        Write the final research report.

        Research question:

        {question}

        Use the research, fact-checking and analysis
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
        - Preserve important uncertainty.
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

    # Crew

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
:::

### Important

Your previous file had:

```text
def build_crew(status_callback=None):
