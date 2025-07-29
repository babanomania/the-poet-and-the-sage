import json
import re
from pathlib import Path
from typing import Dict, List

from .lc_base import LCBaseAgent

class WebBrowsingAgent(LCBaseAgent):
    """Retrieve simplified Wikipedia data from local samples or API."""

    def __init__(self) -> None:
        super().__init__("{text}")

    DATA_DIR = Path(__file__).resolve().parents[1] / "data"

    def sanitize_title(self, title: str) -> str:
        title = title.replace(" ", "_")
        title = re.sub(r"[^A-Za-z0-9_()]+", "", title)
        return title

    def load_local(self, sanitized: str) -> Dict:
        path = self.DATA_DIR / f"{sanitized}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        raise FileNotFoundError(f"No local data for {sanitized}")

    def run(self, query: str) -> Dict:
        sanitized = self.sanitize_title(query)
        try:
            import requests  # lazy import
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{sanitized}"
            sections_url = f"https://en.wikipedia.org/api/rest_v1/page/mobile-sections/{sanitized}"
            summary_resp = requests.get(summary_url, timeout=5)
            summary_resp.raise_for_status()
            sections_resp = requests.get(sections_url, timeout=5)
            sections_resp.raise_for_status()
            data = sections_resp.json()
            sections: List[Dict] = []
            for sec in data.get("remaining", {}).get("sections", [])[:4]:
                sections.append({"heading": sec.get("line", ""), "content": sec.get("text", "")})
            if not sections:
                raise ValueError("No sections from API")
            return {
                "page_title": sanitized.replace("_", " "),
                "sections": sections,
                "source_url": f"https://en.wikipedia.org/wiki/{sanitized}"
            }
        except Exception:
            # Fallback to local sample
            local = self.load_local(sanitized)
            return {
                "page_title": local["title"],
                "sections": local["sections"][:4],
                "source_url": local["source_url"]
            }
