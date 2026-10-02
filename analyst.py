from crewai import Agent

from tools import CalculatorTool


def create_analyst(llm, step_callback=None):

    calculator = CalculatorTool()

    return Agent(
        role="Research Analyst",

        goal=(
            "Turn verified research into a structured, evidence-based analysis. "
            "Identify patterns, important findings, disagreements, and limitations."
        ),

        backstory=(
            "You are a critical research analyst. "
            "You work from the research and fact-checking evidence provided to you. "
            "You do not invent missing information. "
            "When numerical claims require verification, use the calculator."
        ),

        llm=llm,

        tools=[
            calculator,
        ],

        allow_delegation=False,
        verbose=False,
        max_iter=6,
        max_retry_limit=2,
        step_callback=step_callback,
    )
