
from pathlib import Path

import requests

OWNER = "langchain-ai"
REPO = "docs"
BRANCH = "main"
TARGET_DIR = "src/oss/deepagents"
OUTPUT_DIR = Path("data/deepagents")

API_URL = (
    f"https://api.github.com/repos/"
    f"{OWNER}/{REPO}/git/trees/{BRANCH}"
)

RAW_BASE_URL = (
    f"https://raw.githubusercontent.com/"
    f"{OWNER}/{REPO}/{BRANCH}/"
)


def main():
    response = requests.get(
        API_URL,
        params={"recursive": "1"},
        timeout=60,
    )
    response.raise_for_status()

    tree_data = response.json()

    if tree_data.get("truncated"):
        raise RuntimeError(
            "Árvore incompleta. Será necessário "
            "percorrer as subárvores separadamente."
        )

    files = [
        item["path"]
        for item in tree_data["tree"]
        if item["type"] == "blob"
        and item["path"].startswith(TARGET_DIR + "/")
        and item["path"].lower().endswith(".mdx")
    ]

    print(f"Total de arquivos MDX: {len(files)}")

    session = requests.Session()

    for file_path in files:
        url = RAW_BASE_URL + file_path

        result = session.get(url, timeout=30)
        result.raise_for_status()

        relative_path = file_path.removeprefix(
            TARGET_DIR + "/"
        )
        destination = OUTPUT_DIR / relative_path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            result.text,
            encoding="utf-8",
        )

        print(f"Baixado: {relative_path}")

    print(f"\nConcluído. Arquivos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
