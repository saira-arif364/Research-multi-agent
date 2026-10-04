from crewai import Agent


def create_analyst(llm, step_callback=None):

    return Agent(
        role="Research Analyst",
        goal=(
            "Analyze verified research findings and identify the most "
            "important insights, patterns, comparisons, and limitations."
        ),
        backstory=(
            "You are an analytical research specialist. You focus on verified "
            "evidence and turn research findings into clear and useful insights."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_iter=2,
        max_retry_limit=1,
        step_callback=step_callback,
    )
