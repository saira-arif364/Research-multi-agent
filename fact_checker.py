from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, TavilySearchTool


def create_fact_checker(llm, tools=None, step_callback=None):

    if tools is None:
        tools = [
            TavilySearchTool(),
            ScrapeWebsiteTool(),
        ]

    return Agent(
        role="Senior Fact Checker",
        goal=(
            "Verify important claims using reliable sources, identify "
            "unsupported or inaccurate information, and clearly distinguish "
            "verified facts from uncertainty."
        ),
        backstory=(
            "You are a rigorous fact-checking specialist. "
            "You independently verify claims using trustworthy web sources. "
            "You pay particular attention to dates, numbers, recent developments, "
            "source quality, contradictions, and outdated information. "
            "You never invent evidence or citations."
        ),
        llm=llm,
        tools=tools,
        allow_delegation=False,
        verbose=False,
        max_iter=8,
        max_retry_limit=2,
        step_callback=step_callback,
    )
