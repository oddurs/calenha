"""Finding the language on disk."""

from __future__ import annotations

import os
from pathlib import Path


def lang_dir(start: Path | None = None) -> Path:
    """The ``lang/`` directory.

    Uses ``$CALENHA_LANG`` if set; otherwise walks up from ``start`` (or the working
    directory) looking for ``lang/phonology.toml``; otherwise falls back to the copy
    beside this source tree.
    """
    if env := os.environ.get("CALENHA_LANG"):
        return Path(env)
    here = (start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if (folder / "lang" / "phonology.toml").is_file():
            return folder / "lang"
    return Path(__file__).resolve().parents[2] / "lang"
