from typing import Dict

class CritiqueAgent:
    """Review poem quality and suggest revisions."""

    def run(self, poem: str, themes: list, emotions: list) -> Dict:
        approved = True
        feedback = "Beautiful."
        if not poem or len(poem.splitlines()) < 3:
            approved = False
            feedback = "Poem is too short. Expand imagery."
        if not any(theme.lower() in poem.lower() for theme in themes):
            approved = False
            feedback = "Bring themes into focus." if approved else feedback + " Also mention themes."
        return {"approved": approved, "feedback": feedback}
