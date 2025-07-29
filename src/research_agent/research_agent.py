import toml
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class ResearchAgent:
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

    def research(self, text: str) -> dict:
        """
        Synthesizes raw text into a summary, timeline, and key figures.
        """
        summary_prompt = ChatPromptTemplate.from_template("Summarize the following text:\n\n{text}")
        timeline_prompt = ChatPromptTemplate.from_template("Create a timeline of events from the following text:\n\n{text}")
        key_figures_prompt = ChatPromptTemplate.from_template("Identify the key figures in the following text:\n\n{text}")

        output_parser = StrOutputParser()

        summary_chain = summary_prompt | self.llm | output_parser
        timeline_chain = timeline_prompt | self.llm | output_parser
        key_figures_chain = key_figures_prompt | self.llm | output_parser

        summary = summary_chain.invoke({"text": text})
        timeline = timeline_chain.invoke({"text": text})
        key_figures = key_figures_chain.invoke({"text": text})

        return {
            "summary": summary,
            "timeline": timeline,
            "key_figures": key_figures,
        }