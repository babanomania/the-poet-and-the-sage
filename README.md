# 🌸 The Poet and the Sage

> *"Computers can calculate faster than you. They’ll never forget what you teach them. But remember, they’ll never write poetry like Rabindranath Tagore."*  
> — My childhood computer teacher, sometime in 2000

I still remember the pause in the room after he said that; the kind of silence that makes you wonder whether you're learning machines, or learning yourself.

For years, those words stayed with me. Not as a challenge, but as a truth.  
Tagore wasn’t just a poet. He was a **seer**, a **sage**, a **symphony** of nature and soul. His poetry wasn’t code; it was **longing turned into language**.

And yet, here we are.

**The Poet and the Sage** is a meditation on that very moment. Built with Google’s Agent-to-Agent (A2A) framework, this project doesn’t claim to replicate Tagore. It tries, instead, to **listen like him**.

A network of agents — the researcher, the dreamer, the critic — work together to take a seed of history or emotion, and nurture it into something that **feels almost human**, almost sacred. A poem.

Not to replace Tagore. But to remember that even machines can learn to **pause**, to **wonder**, and maybe, just maybe, to **weep**.

## Project Highlights

- **Wikipedia WebBrowsingAgent**: Queries Wikipedia to fetch structured historical or philosophical context
- **Research Agent**: Synthesizes raw Wikipedia text into meaningful summaries, timelines, and figures
- **Context Agent**: Translates facts into symbolic, emotional, and thematic material for poetry
- **Poet Agent**: Writes free verse inspired by Tagore’s tone, emotion, and rhythm
- **Critique Agent**: Reviews and revises output using a cyclic agent feedback loop
- **Traceable Reasoning**: Every poem is born from citations, transformations, and structured thought

## Agent Architecture (Google A2A)

### Agents Overview

| Agent Name         | Responsibility                                                      |
|--------------------|-----------------------------------------------------------------------|
| `WebBrowsingAgent` | Queries Wikipedia and retrieves key article sections                 |
| `ResearchAgent`    | Synthesizes Wikipedia sections into summary, timeline, and figures   |
| `ContextAgent`     | Extracts emotional and symbolic resonance from the research summary  |
| `PoetAgent`        | Composes Tagore-style free verse using themes and metaphors          |
| `CritiqueAgent`    | Provides feedback and requests revision if the poem lacks depth      |

### Flow Diagram

```mermaid
flowchart TD
    UserPrompt --> WebBrowsingAgent
    WebBrowsingAgent --> ResearchAgent
    ResearchAgent --> ContextAgent
    ContextAgent --> PoetAgent
    PoetAgent --> CritiqueAgent
    CritiqueAgent -->|Revise| PoetAgent
    CritiqueAgent -->|Approve| FinalOutput
````

## Example Use Case

**Input Prompt**:

> “Compose a poem about the fall of Constantinople in Tagore's voice.”

**Generated Poem**:

```text
The walls wept before the sea did,  
And in the hush of twilight’s prayer,  
Faith fell not to fire, but to silence,  
Where once hymns echoed, now only dust remembers.
```

**Agent Trace**:

* `WebBrowsingAgent`: Retrieved article sections on the siege and aftermath
* `ResearchAgent`: Synthesized summary, highlighted key figures and consequences
* `ContextAgent`: Extracted themes of mourning, rebirth, silence
* `PoetAgent`: Generated 4-line poem
* `CritiqueAgent`: Approved with minor metaphor alignment suggestions

## Tech Stack

* **Google A2A Framework** – For orchestrating structured multi-agent workflows
* **Gemini 1.5 / GPT-4o** – Backend LLMs for contextual, creative, and poetic reasoning
* **Wikipedia API** – Source of truth for historical/philosophical grounding
* **Custom Prompt Templates** – Each agent has its own refined voice and objective
* *(Optional)* LangGraph – For local simulation or fallback mode

## Use Cases

* **Education**: Teach history and philosophy through poetic distillation
* **Digital Humanities**: Blend AI and literature for interpretive archiving
* **Emotional AI**: Let facts give birth to feeling
* **Cultural Companion Apps**: Converse with the "Poet" or the "Sage"

## Future Roadmap

* [ ] Add Bangla-language output with transliteration support
* [ ] Fine-tune a custom model on Tagore’s corpus for deeper stylistic fidelity
* [ ] Integrate vector memory to retain poetic motifs and metaphor reuse
* [ ] Add voice selector for blending Tagore + other mystic voices (e.g., Faiz, Ghalib)

## License

MIT License. You are free to remix, share, and build on this project with attribution.

## Inspired By

This project is a humble tribute to the soul of **Rabindranath Tagore**, whose words have not merely filled pages but **swept across hearts like monsoon winds through Shantiniketan trees**.

It draws breath from:

* The **divine longing** of *Gitanjali*, where every poem is a whispered offering to the infinite
* The **gentle rebellion** of *Shesher Kobita*, where love dances with intellect
* The **spiritual clarity** of *Sadhana*, where philosophy dissolves into poetry
* The belief that even machines can one day learn to pause, reflect, and write with **a trembling hand touched by the eternal**

We are but messengers, letting the **Poet and the Sage** speak again — not through ink, but through silicon and silence.
