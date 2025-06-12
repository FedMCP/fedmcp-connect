"""Thin helper around Palantir Foundry’s GraphQL endpoint.

Environment variables
---------------------
FOUNDRY_GQL   – full URL to the /api/v2/graphQL endpoint
FOUNDRY_PAT   – personal‑access token with at least read‑only scope
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

import requests

# ---------------------------------------------------------------------------

FOUNDRY_URL: str = os.getenv("FOUNDRY_GQL") or "https://acme.foundry.mil/api/v2/graphQL"
FOUNDRY_TOKEN: str | None = os.getenv("FOUNDRY_PAT")

if not FOUNDRY_TOKEN:  # fail fast – accidental unauth’ed calls are bad
    raise RuntimeError(
        "FOUNDRY_PAT not set – export a Foundry Personal‑Access Token first"
    )

HEADERS: Dict[str, str] = {
    "Authorization": f"Bearer {FOUNDRY_TOKEN}",
    "Accept": "application/json",
}

# ---------------------------------------------------------------------------


def run_query(
    query: str,
    variables: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Execute a GraphQL query against Foundry and return the raw JSON response.

    Parameters
    ----------
    query:
        GraphQL query string.
    variables:
        Optional dict of GraphQL variables.
    timeout:
        Per‑request timeout in seconds (defaults to 30 s).

    Raises
    ------
    RuntimeError
        If the request fails at HTTP or connection level.
    """
    payload = {"query": query, "variables": variables or {}}

    try:
        response = requests.post(
            FOUNDRY_URL,
            json=payload,
            headers=HEADERS,
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logging.exception("Foundry GraphQL request failed")
        raise RuntimeError("Foundry GraphQL request failed") from exc

    return response.json()