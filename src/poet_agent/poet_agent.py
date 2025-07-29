
import toml
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class PoetAgent:
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

    def write_poem(self, themes: list[str]) -> str:
        """
        Writes a poem in the style of Tagore, inspired by the given themes.
        """
        prompt = ChatPromptTemplate.from_template("Write a short, free-verse poem in the style of Rabindranath Tagore about the following themes: {themes}. Do not use any markdown.")
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        return chain.invoke({"themes": ", ".join(themes)})
