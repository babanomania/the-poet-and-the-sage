## Project Name: The Poet and the Sage

This project uses the Google A2A framework to generate poetry in the voice of Rabindranath Tagore, based on deep contextual understanding of historical or philosophical topics. It now supports real-time research via a web browsing agent.

## Agent Descriptions

### 1. WebBrowsingAgent (Wikipedia Edition)

**Purpose**: Queries Wikipedia to retrieve detailed summaries and sections relevant to a historical or philosophical topic.

**Inputs**:
- `query` (string): The topic to search on Wikipedia

**Outputs**:
- `page_title` (string): Title of the retrieved Wikipedia page
- `sections` (array): Each section includes:
  - `heading` (string)
  - `content` (string)
- `source_url` (string): Canonical Wikipedia page link

> Notes:
> - Wikipedia API will be used (e.g., `action=query&prop=extracts`)
> - Ensure output includes 2–4 key sections (not entire page)

### 2. ResearchAgent

**Purpose**: Synthesizes the Wikipedia content into a concise summary, timeline, and key figures.

**Inputs**:
- `sections` (array of `heading`, `content`)
- `page_title` (string)

**Outputs**:
- `summary` (string)
- `key_figures` (array)
- `timeline` (string)

### 3. ContextAgent

**Purpose**: Translates research output into emotional and symbolic context for poetry.

**Inputs**:
- `summary`
- `key_figures`
- `timeline`

**Outputs**:
- `narrative_context` (string)
- `themes` (array)
- `emotions` (array)
- `symbols` (array)

### 4. PoetAgent

**Purpose**: Writes Tagore-style free verse using narrative and symbolic context.

**Inputs**:
- `narrative_context`
- `themes`
- `emotions`
- `symbols`

**Outputs**:
- `poem` (string)

### 5. CritiqueAgent

**Purpose**: Reviews poem quality and suggests revisions based on poetic depth and style alignment.

**Inputs**:
- `poem`
- `themes`
- `emotions`

**Outputs**:
- `approved` (boolean)
- `feedback` (string)

---

## Invocation Order

User → WebBrowsingAgent → ResearchAgent → ContextAgent → PoetAgent ↔ CritiqueAgent → Final Output

All agents operate with structured JSON schemas and reusable prompt templates.
