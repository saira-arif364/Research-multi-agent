from crewai import Agent
from crewai_tools import TavilySearchTool


def create_researcher(llm, tools=None, step_callback=None):

    if tools is None:
        tools = [
            TavilySearchTool(),
        ]

    return Agent(
        role="Research Specialist",
        goal=(
            "Find accurate, recent, relevant information about the research "
            "question using reliable web sources."
        ),
        backstory=(
            "You are a careful research specialist. You search the web, "
            "prefer trustworthy sources, collect important evidence, and "
            "avoid unsupported claims."
        ),
        llm=llm,
        tools=tools,
        allow_delegation=False,
        verbose=False,
        max_iter=3,
        max_retry_limit=1,
        step_callback=step_callback,
    )
