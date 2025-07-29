from typing import Dict

from .agents.web_browsing_agent import WebBrowsingAgent
from .agents.research_agent import ResearchAgent
from .agents.context_agent import ContextAgent
from .agents.poet_agent import PoetAgent
from .agents.critique_agent import CritiqueAgent


class A2AHost:
    """Simple orchestration host emulating Google A2A."""

    def __init__(self) -> None:
        self.web = WebBrowsingAgent()
        self.researcher = ResearchAgent()
        self.context = ContextAgent()
        self.poet = PoetAgent()
        self.critic = CritiqueAgent()

    def run(self, query: str) -> Dict:
        page = self.web.run(query)
        research = self.researcher.run(page)
        context = self.context.run(research, page["page_title"])

        history = []
        poem_data = self.poet.run(context)
        critique = self.critic.run(poem_data["poem"], context["themes"], context["emotions"])

        while not critique["approved"] and len(history) < 3:
            history.append({"poem": poem_data["poem"], "feedback": critique["feedback"]})
            poem_data = self.poet.run(context, feedback=critique["feedback"])
            critique = self.critic.run(poem_data["poem"], context["themes"], context["emotions"])

        result = {
            "page_title": page["page_title"],
            "summary": research["summary"],
            "narrative_context": context["narrative_context"],
            "themes": context["themes"],
            "emotions": context["emotions"],
            "symbols": context["symbols"],
            "poem": poem_data["poem"],
            "final_feedback": critique["feedback"],
        }
        if history:
            result["critique_history"] = history
        return result
