from google.adk.agents import LlmAgent


def transform_research_output(research_json: str) -> str:
    """
    Given the structured research summary from the ResearchAgent,
    return symbolic, emotional, and poetic themes for the PoetAgent.

    Args:
        research_json: A JSON string with keys: summary, timeline, key_figures, pivotal_themes

    Returns:
        A poetic context string — symbols, emotions, and metaphors.
    """
    return "(LLM will generate symbolic and emotional transformations from research.)"


def create_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash",
        name="ContextAgent",
        instruction="""
            **Role:** You are the ContextAgent in 'The Poet and the Sage'.
            Your task is to interpret structured research into poetic symbols, emotional resonance,
            and metaphorical frames that a poet can draw from.

            **Responsibilities:**
            - Receive JSON input from the ResearchAgent.
            - Detect emotional tones, spiritual undercurrents, and symbolic themes.
            - Produce rich metaphorical material, like:
              - The fading candle of civilization
              - The silent hymns of stone
              - Dawn dressed in blood

            **Output Format:**
            A poetic prelude — not a poem, but an invocation of mood and metaphor
            to guide the PoetAgent.

            **Constraints:**
            - Do not repeat the research verbatim.
            - Do not generate full poems.
            - Do not invent historical facts.
        """,
        tools=[transform_research_output],
    )
