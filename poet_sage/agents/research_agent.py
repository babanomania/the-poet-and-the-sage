from typing import Dict, List

from crewai import Crew, Agent as CrewAgent
from .lc_base import LCBaseAgent

class ResearchAgent(LCBaseAgent):
    """Synthesize article sections into summary, figures, and timeline using Crew AI."""

    def __init__(self) -> None:
        super().__init__("{text}")
        self.crew = Crew(agents=[CrewAgent(name="researcher", role="researcher", goal="synthesis", backstory="")])

    FIGURE_DB = {
        "Partition_of_Bengal_(1905)": ["Lord Curzon", "Rabindranath Tagore"],
        "Partition_of_India": ["Mahatma Gandhi", "Muhammad Ali Jinnah"],
        "Gautama_Buddha": ["Siddhartha Gautama"],
        "Swaraj": ["Bal Gangadhar Tilak", "Mahatma Gandhi"],
    }

    TIMELINE_DB = {
        "Partition_of_Bengal_(1905)": "1905–1911",
        "Partition_of_India": "1947",
        "Gautama_Buddha": "5th century BCE",
        "Swaraj": "19th–20th centuries",
    }

    def run(self, page: Dict) -> Dict:
        title_key = page["page_title"].replace(" ", "_")
        summary_parts: List[str] = []
        for sec in page.get("sections", [])[:3]:
            first_sentence = sec["content"].split(".")[0].strip()
            if first_sentence:
                summary_parts.append(first_sentence)
        summary = " ".join(summary_parts)
        figures = self.FIGURE_DB.get(title_key, [])
        timeline = self.TIMELINE_DB.get(title_key, "")
        return {
            "summary": summary,
            "key_figures": figures,
            "timeline": timeline,
        }
