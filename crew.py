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
        raise ValueError("GROQ_API_KEY is missing.")

    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY is missing.")

    llm = LLM(
        model=MODEL_NAME,
        temperature=0.2,
        max_completion_tokens=700,
    )

    # Only the Researcher uses web search.
    search_tool = TavilySearchTool()

    researcher = create_researcher(
        llm=llm,
        tools=[search_tool],
        step_callback=status_callback,
    )

    # Fact checker does NOT search again.
    fact_checker = create_fact_checker(
        llm=llm,
        tools=[],
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

Use web search to find the most important and recent information.

Focus on:
- Key facts
- Important evidence
- Recent developments
- Important numbers or dates
- Reliable sources

Return a concise research brief.

Do not invent facts or sources.
""",
        expected_output="""
A concise research brief containing key findings,
evidence, source names, and URLs.
""",
        agent=researcher,
    )

    fact_check_task = Task(
        description="""
Fact-check the research brief below.

Question:
{question}

Research:
{research_task}

Review the claims using the information provided.

Identify:
- VERIFIED claims
- PARTIALLY VERIFIED claims
- UNSUPPORTED claims
- OUTDATED or uncertain information

Do not invent new facts.

Keep the response short.
""",
        expected_output="""
A concise fact-check report listing the most important
claims and their verification status.
""",
        agent=fact_checker,
        context=[research_task],
    )

    analysis_task = Task(
        description="""
Analyze the research and fact-check report.

Question:
{question}

Research:
{research_task}

Fact check:
{fact_check_task}

Focus on:
- Main findings
- Important patterns
- Useful comparisons
- Limitations

Use only information supported by the previous work.
""",
        expected_output="""
A concise analytical summary of the main findings,
patterns, comparisons, and limitations.
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

Create a concise Markdown report with:

# Research Title

## Executive Summary

## Key Findings

## Analysis

## Limitations

## Conclusion

## Sources

Do not invent facts, citations, or URLs.
""",
        expected_output="""
A polished Markdown research report.
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
