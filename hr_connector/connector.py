"""HR Connector – Workday demo stub for FedMCP.

Exposes a single `/employee` endpoint that fetches (mock) data from Workday.
Replace the `_get_from_workday` helper with real API calls once creds are set.
"""
from __future__ import annotations

import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Workday HR Connector", version="0.1.0")

WORKDAY_TOKEN = os.getenv("WORKDAY_TOKEN", "DEMO_TOKEN")
BASE_URL = os.getenv("WORKDAY_URL", "https://api.workday.com/")


class EmployeeRequest(BaseModel):
    employee_id: str = Field(..., example="12345")


class EmployeeResponse(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    hire_date: datetime
    status: str


async def _get_from_workday(emp_id: str) -> dict[str, str]:
    """Placeholder for a real Workday REST request."""
    # In real life you'd call Workday REST/GraphQL here.
    if emp_id != "12345":
        raise KeyError
    return {
        "first_name": "Alice",
        "last_name": "Zimmer",
        "hire_date": "2020-05-04T00:00:00Z",
        "status": "active",
    }


@app.post("/employee", response_model=EmployeeResponse)
async def get_employee(req: EmployeeRequest):
    """Return an employee record from Workday (mock)."""
    try:
        data = await _get_from_workday(req.employee_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"employee_id": req.employee_id, **data}
