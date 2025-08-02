import logging
import os
import sys

import httpx
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import PoetAgent
from agent_executor import PoetAgentExecutor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    pass

def main():
    host = "localhost"
    port = 10004

    try:
        if not os.getenv("GOOGLE_API_KEY"):
            raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")

        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="compose_poem",
            name="Tagore-style Poetry Generator",
            description="Composes short free verse in the emotional and lyrical style of Rabindranath Tagore.",
            tags=["poetry", "Tagore", "creative"],
            examples=["Write a poem about silence and rain in Tagore's style."]
        )

        agent_card = AgentCard(
            name="Poet Agent",
            description="Composes emotional free verse poetry using symbolic context provided by prior agents.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=PoetAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=PoetAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=PoetAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=host, port=port)

    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
