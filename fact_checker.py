from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, TavilySearchTool


def create_fact_checker(llm, step_callback=None):

    search_tool = TavilySearchTool()
    scraper_tool = ScrapeWebsiteTool()

    return Agent(
        role="Research Fact Checker",

        goal=(
            "Verify important claims from the research, identify unsupported "
            "statements, detect contradictions, and assess source quality."
        ),

        backstory=(
            "You are a rigorous fact checker. "
            "You do not automatically trust the researcher's claims. "
            "You independently verify important facts, compare sources, "
            "identify outdated information, and clearly flag uncertainty."
        ),

        llm=llm,

        tools=[
            search_tool,
            scraper_tool,
        ],

        allow_delegation=False,
        verbose=False,
        max_iter=8,
        max_retry_limit=2,
        step_callback=step_callback,
    )
