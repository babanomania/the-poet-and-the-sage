## Agent Tasks

- [x] Implement `WebBrowsingAgent` using Wikipedia API (e.g., `https://en.wikipedia.org/api/rest_v1/page/summary/{topic}`)
- [x] Support fallback to local summary if Wikipedia page not found
- [x] Limit sections to 3–4 most relevant (e.g., Intro, History, Legacy, Cultural Impact)

## Prompt Adaptations

- [x] Update `research_prompt.txt` to assume full article sections rather than mixed snippets
- [x] Include instruction in `context_prompt.txt` to draw emotional insight from a more encyclopedic tone
- [x] Refine `poet_prompt.txt` to rely more on `narrative_context`

## Agent Control

- [x] Add retry cycle between PoetAgent and CritiqueAgent
- [x] Store critique feedback and show delta between original and final poem

## Example Test Cases

- [x] “Write a poem about the Partition of Bengal” → Pulls from `Partition_of_Bengal_(1905)` and `Partition_of_India`
- [x] “Reflect on the teachings of Buddha” → Uses `Gautama_Buddha`
- [x] “Capture the idea of Swaraj” → Searches `Swaraj` page

## Safety and Boundaries

- [x] Sanitize Wikipedia titles before request
- [x] Graceful handling of disambiguation or missing pages

## Optional Add-ons

- [ ] Add Bengali transliteration or translation toggle
- [ ] Render full trace log with Wikipedia source links and poem
