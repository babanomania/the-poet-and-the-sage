from typing import Dict, List

from .lc_base import LCBaseAgent

class ContextAgent(LCBaseAgent):
    """Map research output into themes, emotions, and symbols."""

    def __init__(self) -> None:
        super().__init__("{text}")

    CONTEXT_DB = {
        "Partition_of_Bengal_(1905)": {
            "themes": ["unity", "resistance"],
            "emotions": ["sorrow", "hope"],
            "symbols": ["song", "river"],
        },
        "Partition_of_India": {
            "themes": ["loss", "rebirth"],
            "emotions": ["grief", "longing"],
            "symbols": ["border", "home"],
        },
        "Gautama_Buddha": {
            "themes": ["awakening", "compassion"],
            "emotions": ["peace", "wonder"],
            "symbols": ["bodhi tree", "path"],
        },
        "Swaraj": {
            "themes": ["self-rule", "discipline"],
            "emotions": ["determination", "reverence"],
            "symbols": ["spinning wheel", "flame"],
        },
    }

    def run(self, research: Dict, page_title: str) -> Dict:
        key = page_title.replace(" ", "_")
        ctx = self.CONTEXT_DB.get(key, {"themes": [], "emotions": [], "symbols": []})
        narrative = f"{research['summary']} It involved {', '.join(research['key_figures'])}."
        return {
            "narrative_context": narrative,
            "themes": ctx["themes"],
            "emotions": ctx["emotions"],
            "symbols": ctx["symbols"],
        }
