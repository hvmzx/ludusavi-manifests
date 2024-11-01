from typing import List
from pathlib import Path

import requests
import yaml


PRIMARY_MANIFEST_URL = "https://raw.githubusercontent.com/mtkennerly/ludusavi-manifest/refs/heads/master/data/manifest.yaml"
NON_STEAM_PATH = Path("non-steam-manifest.yml")
NON_STEAM_TEMPLATE = """
---
"": &template
  files:
    "<root>/<storeGameId>/pfx/drive_c/users/Public/Documents":
      tags:
        - save
    "<root>/<storeGameId>/pfx/drive_c/users/steamuser/Documents":
      tags:
        - save
    "<root>/<storeGameId>/pfx/drive_c/users/steamuser/Appdata":
      tags:
        - save
    "<root>/<storeGameId>/pfx/drive_c/users/steamuser/Saved Games":
      tags:
        - save
      when:
        - os: linux
""".strip()


def main() -> None:
    manifest_content = download_primary_manifest()
    manifest: dict = yaml.safe_load(manifest_content)
    titles = list(sorted(manifest.keys()))
    create_non_steam_manifest(titles)


def download_primary_manifest() -> str:
    response = requests.get(PRIMARY_MANIFEST_URL)
    response.raise_for_status()
    return response.text


def create_non_steam_manifest(titles: List[str]) -> None:
    out = NON_STEAM_TEMPLATE + "\n"

    for title in titles:
        escaped = title.replace("\\", "\\\\").replace('"', '\\"')
        out += f'\n"{escaped}": *template'

    out += "\n"

    # Ensure we can parse it as a valid YAML document.
    yaml.safe_load(out)

    NON_STEAM_PATH.write_text(out, "utf-8")


if __name__ == "__main__":
    main()
