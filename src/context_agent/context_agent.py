import toml
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class ContextAgent:
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

    def extract_themes(self, research: dict) -> list[str]:
        """
        Extracts emotional and symbolic themes from the research summary.
        """
        prompt = ChatPromptTemplate.from_template("Extract the emotional and symbolic themes from the following research summary:\n\n{summary}")
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        themes_text = chain.invoke({"summary": research['summary']})
        return [line.strip() for line in themes_text.split("\n") if line.strip()]