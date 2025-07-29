
import argparse
from src.web_browsing_agent.web_browsing_agent import WebBrowsingAgent
from src.research_agent.research_agent import ResearchAgent
from src.context_agent.context_agent import ContextAgent
from src.poet_agent.poet_agent import PoetAgent
from src.critique_agent.critique_agent import CritiqueAgent

def main():
    """
    The main function of The Poet and the Sage.
    """
    # Get user input from command-line arguments
    parser = argparse.ArgumentParser(description="Generate a poem about a given topic.")
    parser.add_argument("prompt", type=str, help="The topic for the poem.")
    args = parser.parse_args()
    user_prompt = args.prompt

    # Initialize agents
    web_browser = WebBrowsingAgent()
    researcher = ResearchAgent()
    context_extractor = ContextAgent()
    poet = PoetAgent()
    critic = CritiqueAgent()

    # --- Agent Workflow ---

    # 1. WebBrowsingAgent: Get information from Wikipedia
    print("\n1. WebBrowsingAgent: Searching the web...")
    search_result = web_browser.search(user_prompt)
    print(f"   - Found: {search_result[:100]}...")

    # 2. ResearchAgent: Synthesize the information
    print("\n2. ResearchAgent: Synthesizing information...")
    research_data = researcher.research(search_result)
    print(f"   - Summary: {research_data['summary']}")
    print(f"   - Timeline: {research_data['timeline']}")
    print(f"   - Key Figures: {research_data['key_figures']}")

    # 3. ContextAgent: Extract themes
    print("\n3. ContextAgent: Extracting themes...")
    themes = context_extractor.extract_themes(research_data)
    print(f"   - Themes: {themes}")

    # 4. PoetAgent: Write the poem
    print("\n4. PoetAgent: Writing the poem...")
    poem = poet.write_poem(themes)
    print(f"\n--- Initial Poem ---\n{poem}")

    # 5. CritiqueAgent: Review and revise
    print("\n5. CritiqueAgent: Reviewing the poem...")
    critique = critic.critique(poem)
    print(f"   - Critique: {critique}")

    # Simple feedback loop (revise once)
    if "revise" in critique.lower() or "stronger" in critique.lower():
        print("\n   - Revising poem based on feedback...")
        # In a real A2A system, this would be a more sophisticated loop
        poem = poet.write_poem(themes + ["revised with feedback"]) # Add feedback to themes
        print(f"\n--- Revised Poem ---\n{poem}")

    print("\n--- Final Poem ---")
    print(poem)

if __name__ == "__main__":
    main()
