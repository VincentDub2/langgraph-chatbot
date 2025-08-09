from __future__ import annotations

from pathlib import Path
from typing import List, Optional


class PromptManager:
    """Load Markdown prompt templates by name and version.

    Prompts are stored in a directory with files named ``{name}_v{version}.md``.
    The highest numeric version is considered the latest.
    """

    def __init__(self, directory: str = "prompts") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _version_key(self, path: Path) -> int:
        stem = path.stem
        if "_v" in stem:
            try:
                return int(stem.rsplit("_v", 1)[1])
            except ValueError:
                pass
        return 0

    def available_versions(self, name: str) -> List[int]:
        """Return all available versions for ``name`` sorted ascending."""
        files = self.directory.glob(f"{name}_v*.md")
        versions = [self._version_key(p) for p in files]
        return sorted(v for v in versions if v)

    def load(self, name: str, version: Optional[int] = None) -> str:
        """Load a prompt by ``name`` and ``version``.

        If ``version`` is ``None``, the highest available version is loaded.
        """
        if version is None:
            versions = self.available_versions(name)
            if not versions:
                raise FileNotFoundError(f"No prompt versions found for '{name}'")
            version = versions[-1]
        path = self.directory / f"{name}_v{version}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt '{name}' version {version} not found")
        return path.read_text(encoding="utf-8")
