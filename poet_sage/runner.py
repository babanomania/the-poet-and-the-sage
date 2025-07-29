import json
from typing import Dict

from .host import A2AHost


def run_pipeline(query: str) -> Dict:
    host = A2AHost()
    return host.run(query)


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "Gautama Buddha"
    out = run_pipeline(topic)
    print(json.dumps(out, indent=2, ensure_ascii=False))
