from __future__ import annotations

from typing import Type
from urllib.parse import urlparse

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Calculator Tool
# ---------------------------------------------------------

class CalculatorInput(BaseModel):
    expression: str = Field(
        ...,
        description="A mathematical expression such as 125 * 0.18 or 2026 - 2020.",
    )


class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = (
        "Calculate a mathematical expression. "
        "Use this to verify numerical calculations."
    )
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            # Only allow mathematical characters.
            allowed = set("0123456789+-*/().% ")

            if not set(expression) <= allowed:
                return "Invalid mathematical expression."

            result = eval(expression, {"__builtins__": {}}, {})

            return f"{expression} = {result}"

        except Exception as exc:
            return f"Could not calculate expression: {exc}"


# ---------------------------------------------------------
# Source Validator Tool
# ---------------------------------------------------------

class SourceValidatorInput(BaseModel):
    urls: str = Field(
        ...,
        description=(
            "Comma-separated URLs that should be checked for availability."
        ),
    )


class SourceValidatorTool(BaseTool):
    name: str = "Source Validator"
    description: str = (
        "Check whether research source URLs are reachable. "
        "Provide comma-separated URLs."
    )
    args_schema: Type[BaseModel] = SourceValidatorInput

    def _run(self, urls: str) -> str:
        results = []

        for raw_url in urls.split(","):
            url = raw_url.strip()

            if not url:
                continue

            parsed = urlparse(url)

            if parsed.scheme not in {"http", "https"}:
                results.append(f"{url} -> invalid URL")
                continue

            try:
                response = requests.head(
                    url,
                    timeout=8,
                    allow_redirects=True,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 "
                            "(Research AI Source Validator)"
                        )
                    },
                )

                results.append(
                    f"{url} -> HTTP {response.status_code}"
                )

            except Exception as exc:
                results.append(
                    f"{url} -> unavailable ({type(exc).__name__})"
                )

        if not results:
            return "No URLs were provided."

        return "\n".join(results)
