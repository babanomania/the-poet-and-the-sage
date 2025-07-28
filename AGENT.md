## Project Name: The Poet and the Sage

This project uses the Google A2A framework to generate poetry in the voice of Rabindranath Tagore, based on deep contextual understanding of historical or philosophical topics. It now supports real-time research via a web browsing agent.

---

## Agent Descriptions

### 1. WebBrowsingAgent

**Purpose**: Performs deep live research on the given query using web search and document scraping (news, Wikipedia, reports).

**Inputs**:
- `query` (string)

**Outputs**:
- `raw_snippets` (array of objects with fields: `title`, `source`, `snippet`)
- `source_links` (array of URLs)

---

### 2. ResearchAgent

**Purpose**: Synthesizes web snippets into a concise factual overview.

**Inputs**:
- `raw_snippets`
- `source_links`

**Outputs**:
- `summary` (string)
- `key_figures` (array)
- `timeline` (string)

---

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

---

### 4. PoetAgent

**Purpose**: Writes Tagore-style free verse using narrative and symbolic context.

**Inputs**:
- `narrative_context`
- `themes`
- `emotions`
- `symbols`

**Outputs**:
- `poem` (string)

---

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
