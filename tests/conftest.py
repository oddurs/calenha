from pathlib import Path

import pytest

from calenha.phonology import Phonology

LANG = Path(__file__).resolve().parents[1] / "lang"


@pytest.fixture(scope="session")
def lang_path() -> Path:
    return LANG


@pytest.fixture(scope="session")
def phonology() -> Phonology:
    return Phonology.load(LANG / "phonology.toml")
