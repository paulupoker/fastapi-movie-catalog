import os
import pathlib
import sys

import pytest


@pytest.mark.skip(reason="user schema not implemented yet")
def test_user_schema() -> None:
    user_data = {"username": "foo"}
    assert user_data["username"] == "bar"


@pytest.mark.skipif(
    sys.platform == "win32", reason="skip test on Windows due to some reason"
)
def test_platform() -> None:
    assert sys.platform != "win32"


@pytest.mark.skipif(os.name != "nt", reason="run only on Windows")
def test_only_fow_windows() -> None:
    path = pathlib.Path(__file__)
    assert isinstance(path, pathlib.WindowsPath)


@pytest.mark.skipif(os.uname().machine != "arm64", reason="run only on arm64 arch")
def test_only_for_arm64() -> None:
    arch = os.uname().machine
    assert arch == "arm64"
