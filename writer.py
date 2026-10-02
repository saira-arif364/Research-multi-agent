from crewai import Agent

from tools import SourceValidatorTool


def create_writer(llm, step_callback=None):

    source_validator = SourceValidatorTool()

    return Agent(
        role="Senior Research Writer",

        goal=(
            "Produce a clear, professional, well-structured research report "
            "based only on the verified research and analysis."
        ),

        backstory=(
            "You are an experienced research writer. "
            "You transform complex research into readable reports. "
            "You preserve important uncertainty and disagreements. "
            "You never fabricate citations, URLs, statistics, quotations, "
            "or source names."
        ),

        llm=llm,

        tools=[
            source_validator,
        ],

        allow_delegation=False,
        verbose=False,
        max_iter=6,
        max_retry_limit=2,
        step_callback=step_callback,
    )
