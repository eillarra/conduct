import os
import pytest


@pytest.fixture()
def files_path() -> str:
    """Path to test files."""
    return os.path.join(
        os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "files"
    )
