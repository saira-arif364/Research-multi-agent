from crewai import Agent


def create_writer(llm, step_callback=None):

    return Agent(
        role="Research Report Writer",
        goal=(
            "Turn verified research and analysis into a clear, professional "
            "and concise research report."
        ),
        backstory=(
            "You are an experienced research writer. You communicate complex "
            "information clearly, preserve uncertainty, and never invent facts "
            "or sources."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_iter=2,
        max_retry_limit=1,
        step_callback=step_callback,
    )
