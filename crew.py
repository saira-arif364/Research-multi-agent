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
        max_completion_tokens=300,
    )

    # Only the Researcher searches the web.
    search_tool = TavilySearchTool()

    researcher = create_researcher(
        llm=llm,
        tools=[search_tool],
        step_callback=status_callback,
    )

    # Fact Checker reviews the Researcher's output.
    # It does not perform another web search.
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

    # =====================================================
    # RESEARCH TASK
    # =====================================================

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
evidence, source names, and source URLs.
""",
        agent=researcher,
    )

    # =====================================================
    # FACT CHECK TASK
    # =====================================================

    fact_check_task = Task(
        description="""
Fact-check the research produced by the previous agent.

The research question is:

{question}

Review the research carefully.

Identify:
- VERIFIED claims
- PARTIALLY VERIFIED claims
- UNSUPPORTED claims
- OUTDATED or uncertain information

Pay particular attention to important facts,
numbers, dates, and recent claims.

Do not invent new facts.

Keep the response concise.
""",
        expected_output="""
A concise fact-check report listing the most important
claims and their verification status.
""",
        agent=fact_checker,
        context=[
            research_task,
        ],
    )

    # =====================================================
    # ANALYSIS TASK
    # =====================================================

    analysis_task = Task(
        description="""
Analyze the research and fact-checking results.

The research question is:

{question}

Use the previous agents' work as your source material.

Focus on:
- Main findings
- Important patterns
- Useful comparisons
- Important limitations
- Research gaps

Use only information supported by the previous work.

Do not invent information.
""",
        expected_output="""
A concise analytical summary of the main findings,
patterns, comparisons, limitations, and research gaps.
""",
        agent=analyst,
        context=[
            research_task,
            fact_check_task,
        ],
    )

    # =====================================================
    # WRITING TASK
    # =====================================================

    writing_task = Task(
        description="""
Write the final research report.

The research question is:

{question}

Use the research, fact-checking, and analysis provided
by the previous agents.

Create a concise professional Markdown report.

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
A polished Markdown research report.
""",
        agent=writer,
        context=[
            research_task,
            fact_check_task,
            analysis_task,
        ],
    )

    # =====================================================
    # CREW
    # =====================================================

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
