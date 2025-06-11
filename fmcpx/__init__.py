

"""FedMCP Connector SDK

This package provides:
    • `__version__` – semantic version string derived from package metadata.
    • `app`         – Typer CLI instance for the connector generator.

Typical usage from the shell:

    $ python -m fmcpx init my_connector
"""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Final

try:
    __version__: Final[str] = version("fmcpx")
except PackageNotFoundError:  # running from source checkout / editable install
    __version__ = "0.0.0-dev"

# Re‑export the Typer application so callers can embed or extend it.
from .__main__ import app  # noqa: E402  pylint: disable=wrong-import-position

__all__ = ["app", "__version__"]