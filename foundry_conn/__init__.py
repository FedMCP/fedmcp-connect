"""Palantir Foundry connector package.

Importing the top‑level module gives you the two execution helpers:

    >>> from foundry_conn import execute, aexecute
    >>> result = execute({"query": "...", "variables": {...}})
    >>> async for row in aexecute({"query": "..."})

Both functions are re‑exported from *connector.py* so callers don’t
need to know the internal file structure.
"""

from .connector import execute, aexecute  # re‑export

__all__ = ["execute", "aexecute"]