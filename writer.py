from crewai import Agent


def create_writer(llm, step_callback=None):

    return Agent(
        role="Research Report Writer",
        goal="Create a clear and concise final research report.",
        backstory=(
            "You are a professional research writer who presents "
            "verified information clearly and accurately."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_iter=1,
        max_retry_limit=1,
        step_callback=step_callback,
    )
