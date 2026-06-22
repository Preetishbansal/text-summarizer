"""
crew_setup.py

Defines the CrewAI Agent, Task, and Crew.

- Agent: an LLM persona with a role/goal, given access to our custom tool.
- Task: the specific instruction we give the agent for this run.
- Crew: runs the agent against the task and returns the result.

We use Groq as the LLM provider (free tier, OpenAI-compatible API),
via LiteLLM, which CrewAI uses internally. Model strings for LiteLLM
are prefixed with "groq/".
"""

import os
from crewai import Agent, Task, Crew, LLM
from text_tools import analyze_text_stats


def build_crew(user_text: str) -> Crew:
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.0,
    )

    summarizer_agent = Agent(
        role="Text Analyst",
        goal="Produce a heavily condensed summary (1-2 sentences) of the given text.",
        backstory=(
            "You are a meticulous analyst who always grounds your summary "
            "in objective facts. You provide only the final summary."
        ),
        tools=[analyze_text_stats],
        llm=llm,
        verbose=True,
    )

    task = Task(
        description=(
            "Here is the text to process:\n\n"
            f"---\n{user_text}\n---\n\n"
            "Write a highly condensed, highly accurate summary (1-2 sentences max) of the text. "
            "You MUST extract the core, true meaning of the text without losing factual accuracy. "
            "You MUST write a completely new, original summary that is shorter than the input text. "
            "DO NOT just copy or repeat the input text. Provide ONLY the summary."
        ),
        expected_output="A completely original, factually accurate 1-2 sentence summary of the text.",
        agent=summarizer_agent,
    )

    return Crew(agents=[summarizer_agent], tasks=[task], verbose=True)


def run_pipeline(user_text: str) -> str:
    crew = build_crew(user_text)
    result = crew.kickoff()
    return str(result)
