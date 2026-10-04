from crewai import Agent


def create_analyst(llm, step_callback=None):

    return Agent(
        role="Research Analyst",
        goal="Turn verified research into useful insights and conclusions.",
        backstory=(
            "You analyze research findings and identify important "
            "patterns, comparisons, and limitations."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_iter=1,
        max_retry_limit=1,
        step_callback=step_callback,
    )
