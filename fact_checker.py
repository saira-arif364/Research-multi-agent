from crewai import Agent


def create_fact_checker(llm, tools=None, step_callback=None):

    return Agent(
        role="Fact Verification Specialist",
        goal=(
            "Check the research for unsupported, uncertain, "
            "outdated, or inconsistent claims."
        ),
        backstory=(
            "You carefully review research evidence and distinguish "
            "supported information from uncertain claims."
        ),
        llm=llm,
        tools=[],
        allow_delegation=False,
        verbose=False,
        max_iter=1,
        max_retry_limit=1,
        step_callback=step_callback,
    )
