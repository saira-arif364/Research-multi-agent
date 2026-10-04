from crewai import Agent
from crewai_tools import TavilySearchTool


def create_fact_checker(llm, tools=None, step_callback=None):

    if tools is None:
        tools = [
            TavilySearchTool(),
        ]

    return Agent(
        role="Fact Verification Specialist",
        goal=(
            "Verify the most important claims from the research and identify "
            "information that is unsupported, outdated, or uncertain."
        ),
        backstory=(
            "You are a rigorous fact checker. You verify important claims "
            "using trustworthy web sources and clearly separate verified "
            "information from uncertainty."
        ),
        llm=llm,
        tools=tools,
        allow_delegation=False,
        verbose=False,
        max_iter=3,
        max_retry_limit=1,
        step_callback=step_callback,
    )
