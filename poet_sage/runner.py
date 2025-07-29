import difflib
import json
from typing import Dict

from .agents.web_browsing_agent import WebBrowsingAgent
from .agents.research_agent import ResearchAgent
from .agents.context_agent import ContextAgent
from .agents.poet_agent import PoetAgent
from .agents.critique_agent import CritiqueAgent


def run_pipeline(query: str) -> Dict:
    web = WebBrowsingAgent()
    researcher = ResearchAgent()
    contexter = ContextAgent()
    poet = PoetAgent()
    critic = CritiqueAgent()

    page = web.run(query)
    research = researcher.run(page)
    context = contexter.run(research, page["page_title"])

    history = []
    poem_data = poet.run(context)
    critique = critic.run(poem_data["poem"], context["themes"], context["emotions"])

    while not critique["approved"] and len(history) < 3:
        history.append({"poem": poem_data["poem"], "feedback": critique["feedback"]})
        poem_data = poet.run(context, feedback=critique["feedback"])
        critique = critic.run(poem_data["poem"], context["themes"], context["emotions"])

    delta = ""
    if history:
        diff = difflib.unified_diff(history[-1]["poem"].splitlines(), poem_data["poem"].splitlines(), lineterm="")
        delta = "\n".join(diff)
        history[-1]["delta"] = delta

    result = {
        "page_title": page["page_title"],
        "summary": research["summary"],
        "narrative_context": context["narrative_context"],
        "themes": context["themes"],
        "emotions": context["emotions"],
        "symbols": context["symbols"],
        "poem": poem_data["poem"],
        "critique_history": history,
        "final_feedback": critique["feedback"],
    }
    return result


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "Gautama Buddha"
    out = run_pipeline(topic)
    print(json.dumps(out, indent=2, ensure_ascii=False))
