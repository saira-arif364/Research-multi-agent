from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, TavilySearchTool

def create_researcher(llm, tools=None, step_callback=None):

```
# Use tools supplied by crew.py.
# If none are supplied, create the default research tools.
if tools is None:
    tools = [
        TavilySearchTool(),
        ScrapeWebsiteTool(),
    ]

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

    tools=tools,

    allow_delegation=False,

    verbose=False,

    max_iter=8,

    max_retry_limit=2,

    step_callback=step_callback,
)
```
