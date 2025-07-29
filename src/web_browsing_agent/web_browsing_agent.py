import toml
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class WebBrowsingAgent:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchAPIWrapper()
        self.config = toml.load("config.toml")
        self.llm = self._get_llm()

    def _get_llm(self):
        provider = self.config["llm"]["provider"]
        if provider == "google":
            model_name = self.config["llm"]["google"]["model"]
            return ChatGoogleGenerativeAI(model=model_name)
        elif provider == "openai":
            model_name = self.config["llm"]["openai"]["model"]
            return ChatOpenAI(model=model_name)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def search(self, query: str) -> str:
        """
        Searches the web for a given query using DuckDuckGo.
        """
        # For simplicity, we'll directly use the search tool here.
        # In a more complex scenario, you might use a LangChain agent executor
        # with the search tool.
        return self.search_tool.run(query)