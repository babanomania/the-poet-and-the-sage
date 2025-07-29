import toml
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class CritiqueAgent:
    def __init__(self):
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

    def critique(self, poem: str) -> str:
        """
        Reviews a poem and provides feedback for revision.
        """
        prompt = ChatPromptTemplate.from_template("Critique the following poem. Is it emotionally resonant? Does it align with Tagore's style? Provide feedback for revision.\n\n{poem}")
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        return chain.invoke({"poem": poem})
