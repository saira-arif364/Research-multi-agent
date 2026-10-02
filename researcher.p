from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, TavilySearchTool


def create_researcher(llm, step_callback=None):

    search_tool = TavilySearchTool()
    scraper_tool = ScrapeWebsiteTool()

    return Agent(
        role="Senior Web Researcher",

        goal=(
            "Find accurate, recent, relevant information from reliable "
            "web sources and build a strong evidence base for the research question."
        ),

        backstory=(
            "You are a meticulous research specialist. "
            "You search broadly but prefer primary sources, official documentation, "
            "academic papers, reputable organizations, and high-quality journalism. "
            "You distinguish facts from opinions and never invent sources."
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
