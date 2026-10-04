import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

import os

from crewai import Crew, LLM, Process, Task
from crewai_tools import TavilySearchTool

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
        max_completion_tokens=900,
    )

    search_tool = TavilySearchTool()

    researcher = create_researcher(
        llm=llm,
        tools=[search_tool],
        step_callback=status_callback,
    )

    fact_checker = create_fact_checker(
        llm=llm,
        tools=[search_tool],
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
Research this question:

{question}

Find the most important recent facts.

Use reliable sources and focus only on information needed to answer
the question.

Return a concise research brief with:
- Key findings
- Important evidence
- Important dates or numbers
- Source names
- Source URLs

Do not invent information.
""",
        expected_output="""
A concise research brief of approximately 500 words maximum.
""",
        agent=researcher,
    )

    fact_check_task = Task(
        description="""
Fact-check the research brief below.

Question:
{question}

Research brief:
{research_task}

Verify the most important claims using web search.

Focus on:
- Important facts
- Numbers
- Dates
- Recent claims
- Source reliability

For each important claim, classify it as:
VERIFIED
PARTIALLY VERIFIED
CONTRADICTED
UNSUPPORTED
OUTDATED

Keep the report concise.
""",
        expected_output="""
A concise fact-check report of approximately 400 words maximum.
Include claim, status, evidence, and source URL where available.
""",
        agent=fact_checker,
        context=[research_task],
    )

    analysis_task = Task(
        description="""
Analyze the research and fact-checking results.

Question:
{question}

Research:
{research_task}

Fact check:
{fact_check_task}

Focus only on verified or reasonably supported information.

Identify:
- Main findings
- Important patterns
- Useful comparisons
- Important limitations
- Research gaps

Do not invent information.
""",
        expected_output="""
A concise analytical brief of approximately 350 words maximum.
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

Question:
{question}

Research:
{research_task}

Fact check:
{fact_check_task}

Analysis:
{analysis_task}

Create a professional Markdown report.

Use this structure:

# Research Title

## Executive Summary

## Key Findings

## Analysis

## Limitations

## Conclusion

## Sources

Rules:
- Use only supported information.
- Preserve uncertainty.
- Do not invent facts.
- Do not invent citations.
- Do not invent URLs.
- Keep the report concise.
""",
        expected_output="""
A polished Markdown research report of approximately 700 words maximum.
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
