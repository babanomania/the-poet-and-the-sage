# Setup Guide

This project requires Python 3.8 or newer. The only runtime dependency is `requests` for Wikipedia queries.

## 1. Clone the repository

```bash
git clone <repo-url>
cd the-poet-and-the-sage
```

## 2. Create a virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install requests
```

The agents will try to call the Wikipedia API. If your environment does not have internet access, the project falls back to the sample JSON files in `poet_sage/data/`.

## 4. Run the pipeline

Execute the runner module with a topic of your choice:

```bash
python -m poet_sage.runner "Gautama Buddha"
```

This prints a JSON object containing the summary, emotional context and a generated poem.

# Testing Examples

There are no automated unit tests yet, but you can verify the pipeline manually. Here are a few topics to try:

```bash
python -m poet_sage.runner "Gautama Buddha"
python -m poet_sage.runner "Partition of India"
python -m poet_sage.runner "Swaraj"
```

Each command should produce a poem in Tagore's style based on Wikipedia data.
