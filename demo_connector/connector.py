
"""Demo connector – example FedMCP tool service.

Endpoint `/employee` returns a mocked employee record and illustrates how a
real connector would pull from Workday / SuccessFactors, etc.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

app = FastAPI(title="Demo HR Connector", version="0.1.0")

# ────────────────── Pydantic models ──────────────────

class EmployeeRequest(BaseModel):
    employee_id: str = Field(..., example="12345")

class AuditTag(BaseModel):
    tag: str
    value: Any

class EmployeeResponse(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    hire_date: datetime
    status: Literal["active", "terminated"]
    audit_tags: Optional[Dict[str, Any]] = None

# ────────────────── In‑memory demo DB ──────────────────

_DEMO_DB = {
    "12345": {
        "first_name": "Alice",
        "last_name": "Zimmer",
        "hire_date": "2020-05-04T00:00:00Z",
        "status": "active",
    },
    "98765": {
        "first_name": "Bob",
        "last_name": "Kenyon",
        "hire_date": "2018-03-12T00:00:00Z",
        "status": "terminated",
    },
}

# ────────────────── Routes ──────────────────

@app.post("/employee", response_model=EmployeeResponse)
async def get_employee(req: EmployeeRequest, request: Request):
    """Return an employee record (mock), echoing request and showing audit tags."""
    data = _DEMO_DB.get(req.employee_id)
    if not data:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Example audit tags: could be added to a real audit log
    audit_tags = {
        "requested_by": request.client.host if request.client else "unknown",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "purpose": "demo-hr-lookup",
    }

    return {
        "employee_id": req.employee_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "hire_date": data["hire_date"],
        "status": data["status"],
        "audit_tags": audit_tags,
    }
