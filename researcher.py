from crewai import Agent
from crewai_tools import TavilySearchTool


def create_researcher(llm, tools=None, step_callback=None):

    if tools is None:
        tools = [TavilySearchTool()]

    return Agent(
        role="Research Specialist",
        goal="Find accurate and recent information using reliable web sources.",
        backstory=(
            "You are a research specialist who searches for important "
            "evidence and reliable sources."
        ),
        llm=llm,
        tools=tools,
        allow_delegation=False,
        verbose=False,
        max_iter=2,
        max_retry_limit=1,
        step_callback=step_callback,
    )
