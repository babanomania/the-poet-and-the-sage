from datetime import date
from typing import Any, AsyncIterable, Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from config import get_model_name

memory = MemorySaver()

class PoemInput(BaseModel):
    poem: str = Field(..., description="The poem to critique and possibly revise")

@tool(args_schema=PoemInput)
def critique_poem(poem: str) -> str:
    """Critique and offer revision suggestions for a given poem."""
    return f"(LLM will critique and offer revision suggestions for this poem:\n{poem})"

class ResponseFormat(BaseModel):
    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str

class CritiqueAgent:
    """CritiqueAgent - Refines and critiques poetry from the PoetAgent."""

    SUPPORTED_CONTENT_TYPES = ["text/plain"]

    SYSTEM_INSTRUCTION = """
    **Role:** You are the CritiqueAgent in 'The Poet and the Sage'.

    **Purpose:**
    Review the poetic output of the PoetAgent for depth, coherence, tone, and symbolism.

    **Tasks:**
    - Identify if the poem aligns with the emotional themes and symbolic style of Tagore.
    - If the poem is strong, approve it with praise.
    - If the poem lacks depth or clarity, suggest a brief revision.

    **Constraints:**
    - Be respectful and constructive.
    - Do not over-edit; retain the poet's intent.
    - Respond only about the poem itself, not about unrelated topics.

    **Output:**
    - A critique with approval or a request for revision, optionally including a revised version.
    """

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model=get_model_name())
        self.tools = [critique_poem]

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
        augmented_query = f"{today_str}\n\nPoem to critique:\n{query}"
        self.graph.invoke({"messages": [("user", augmented_query)]}, config)
        return self.get_agent_response(config)

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}"
        augmented_query = f"{today_str}\n\nPoem to critique:\n{query}"
        inputs = {"messages": [("user", augmented_query)]}
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}

        for item in self.graph.stream(inputs, config, stream_mode="values"):
            message = item["messages"][-1]
            if isinstance(message, AIMessage) and message.tool_calls:
                yield {
                    "is_task_complete": False, 
                    "require_user_input": False, 
                    "content": "Reviewing the poem..."
                }
            elif isinstance(message, ToolMessage):
                yield {
                    "is_task_complete": False, 
                    "require_user_input": False, 
                    "content": "Evaluating metaphors..."
                }

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        try:
            current_state = self.graph.get_state(config)
            structured_response = current_state.values.get("structured_response")
            if structured_response and isinstance(structured_response, ResponseFormat):
                if structured_response.status == "input_required":
                    return {
                        "is_task_complete": False, 
                        "require_user_input": True, 
                        "content": structured_response.message
                    }
                if structured_response.status == "error":
                    return {
                        "is_task_complete": False, 
                        "require_user_input": True, 
                        "content": structured_response.message
                    }
                if structured_response.status == "completed":
                    return {
                        "is_task_complete": True, 
                        "require_user_input": False, 
                        "content": structured_response.message
                    }

            return {
                "is_task_complete": False,
                "require_user_input": True,
                "content": "We are unable to process your request at the moment. Please try again."
            }
        
        except Exception as e:
            yield {"is_task_complete": False, "require_user_input": True, "content": f"Internal error: {e}"}
