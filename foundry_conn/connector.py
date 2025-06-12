from .foundry import run_query
from fmcpx.kms_jws import sign_response  # import local PEM stub for now
import asyncio

def _build_payload(result: dict) -> dict:
    """Common response construction for sync/async callers."""
    signed = sign_response(result)
    return {
        "data": result,
        "signed_response": signed["jws"],
        "audit_log": [
            {
                "ts": signed["ts"],
                "event": "foundry_query",
                "foundry_request_id": result.get("extensions", {}).get("requestId"),
                "dataset_urn": "urn:palantir:...",  # TODO: refine
            }
        ],
    }

def execute(inputs: dict) -> dict:
    """
    inputs = { "query": "...", "variables": {...} }
    """
    result = run_query(inputs["query"], inputs.get("variables"))
    return _build_payload(result)

async def aexecute(inputs: dict) -> dict:  # noqa: D401
    """
    Async variant that off‑loads the blocking HTTP call to a thread so
    agent runtimes with an event‑loop can `await` it directly.

    Example:
        data = await aexecute({"query": "...", "variables": {...}})
    """
    result = await asyncio.to_thread(
        run_query,
        inputs["query"],
        inputs.get("variables"),
    )
    return _build_payload(result)

__all__ = ["execute", "aexecute"]