import os
from typing import Type
from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import wikipedia

load_dotenv()


# ---------------------- Tool ----------------------

class WikipediaToolInput(BaseModel):
    """Input schema for WikipediaTool."""
    topic: str = Field(..., description="The topic to search on Wikipedia.")


class WikipediaTool(BaseTool):
    name: str = "Wikipedia Research Tool"
    description: str = (
        "Searches for a topic on Wikipedia and returns a concise summary. "
        "Use this to retrieve factual information about well-known topics."
    )
    args_schema: Type[BaseModel] = WikipediaToolInput

    def _run(self, topic: str) -> str:
        try:
            summary = wikipedia.summary(topic, sentences=3)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Topic '{topic}' is ambiguous. Try one of: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{topic}'."
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ---------------------- Agent ----------------------

class WikipediaAgent:
    """Agent that handles Wikipedia research tasks."""

    SUPPORTED_CONTENT_TYPES = ["text/plain"]
    
    def __init__(self):
        """Initializes the WikipediaAgent."""
        if os.getenv("GOOGLE_API_KEY"):
            self.llm = LLM(
                model="gemini/gemini-2.0-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
            )
        else:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        self.research_assistant = Agent(
            role="Wikipedia Research Assistant",
            goal="Answer factual questions by searching Wikipedia.",
            backstory=(
                "You're a research expert who specializes in finding reliable summaries "
                "from Wikipedia. Your job is to answer user questions with accurate, relevant, "
                "and concise information sourced from Wikipedia."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[WikipediaTool()],
            llm=self.llm,
        )

    def invoke(self, question: str) -> str:
        """Executes the Wikipedia research task."""
        task_description = (
            f"Search Wikipedia to answer the user's question: '{question}'. "
            "Use the Wikipedia Research Tool and respond clearly."
        )

        search_task = Task(
            description=task_description,
            expected_output="A clear and concise explanation sourced from Wikipedia.",
            agent=self.research_assistant,
        )

        crew = Crew(
            agents=[self.research_assistant],
            tasks=[search_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        return str(result)
