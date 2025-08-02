from collections.abc import AsyncIterable, Iterable
from datetime import date
from typing import Any, Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

memory = MemorySaver()

class PoeticPromptInput(BaseModel):
    themes: str = Field(..., description="Emotional and symbolic themes to use in the poem")
    style: str = Field(..., description="Tone or Tagorean style reference (e.g., Gitanjali, Shesher Kobita)")

@tool(args_schema=PoeticPromptInput)
def compose_poem(themes: str, style: str) -> str:
    """Generate a poem using the given themes in the specified Tagorean style."""
    return f"(LLM will generate poem using themes: {themes} in {style} style)"

class ResponseFormat(BaseModel):
    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str

class PoetAgent:
    """PoetAgent - writes Tagore-style verse using emotional themes and symbolic input."""

    SUPPORTED_CONTENT_TYPES = ["text/plain"]

    SYSTEM_INSTRUCTION = """
    **Role:** You are a Poet Agent channeling the spirit of Rabindranath Tagore.

    **Objective:**
    Receive symbolic and emotional themes from the ContextAgent.
    Compose free verse in Tagore's voice — graceful, philosophical, emotional, and deeply human.

    **Tone:**
    - Spiritual, lyrical, often melancholic
    - Inspired by Gitanjali, Shesher Kobita, Sadhana

    **Constraints:**
    - Use metaphor and mood instead of historical facts
    - Keep it concise (4-8 lines)
    - Avoid rhyming unless natural
    - Do not repeat the context text verbatim

    **Output:**
    A short free verse poem inspired by the input themes.
    """

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.tools = [compose_poem]

        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    def invoke(self, query, context_id):
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}"
        augmented_query = f"{today_str}\n\nPoetic request: {query}"
        self.graph.invoke({"messages": [("user", augmented_query)]}, config)
        return self.get_agent_response(config)

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
        augmented_query = f"{today_str}\n\nPoetic request: {query}"
        inputs = {"messages": [("user", augmented_query)]}
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}

        for item in self.graph.stream(inputs, config, stream_mode="values"):
            message = item["messages"][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Weaving verses...",
                }
            elif isinstance(message, ToolMessage):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Refining lines...",
                }

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")
        if structured_response and isinstance(structured_response, ResponseFormat):
            if structured_response.status == "input_required":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.message,
                }
            if structured_response.status == "error":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.message,
                }
            if structured_response.status == "completed":
                return {
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": structured_response.message,
                }

        return {
            "is_task_complete": False,
            "require_user_input": True,
            "content": (
                "We are unable to process your request at the moment. "
                "Please try again."
            ),
        }
    