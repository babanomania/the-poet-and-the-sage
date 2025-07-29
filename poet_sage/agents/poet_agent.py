import random
from typing import Dict, Optional

from .lc_base import LCBaseAgent

class PoetAgent(LCBaseAgent):
    """Compose Tagore-style free verse."""

    def __init__(self) -> None:
        super().__init__("{text}")

    def run(self, context: Dict, feedback: Optional[str] = None) -> Dict:
        themes = context.get("themes", [])
        emotions = context.get("emotions", [])
        symbols = context.get("symbols", [])
        narrative = context.get("narrative_context", "")
        lines = []
        if feedback:
            lines.append("Responding to the critic, I breathe again:")
        lines.append(f"In the shadow of the {symbols[0] if symbols else 'memory'}, {themes[0] if themes else ''} stirs.")
        lines.append(f"{narrative.split('.')[0].strip()}.")
        if emotions:
            lines.append(f"It tastes of {emotions[0]} and {emotions[-1]}.")
        lines.append("Silence gathers like evening prayer.")
        poem = "\n".join(lines[:5])
        return {"poem": poem}
