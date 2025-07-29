from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import FakeListLLM


class LCBaseAgent:
    """Minimal LangChain agent wrapper."""

    def __init__(self, template: str = "{text}") -> None:
        self.template = PromptTemplate.from_template(template)
        self.llm = FakeListLLM(responses=[""])
        self.chain = LLMChain(prompt=self.template, llm=self.llm)

    def generate(self, **kwargs):
        self.llm.responses = [kwargs.get("text", "")]
        return self.chain.invoke(kwargs)
