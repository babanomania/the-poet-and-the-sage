import tomli
from pathlib import Path

def get_model_name():
    pyproject_path = Path(__file__).resolve().parents[0] / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomli.load(f)
    return data["tool"]["model_name"]
