from __future__ import annotations

from fastapi import FastAPI, HTTPException
from .models import OffboardingRequest
from .providers import demo_providers
from .workflow import OffboardingWorkflow


workflow = OffboardingWorkflow(demo_providers())
app = FastAPI(title="Cross-Tenant Offboarding")


@app.get("/subjects/{subject}/discover")
def discover(subject: str):
    return workflow.discover(subject)


@app.post("/offboarding/execute")
def execute(request: OffboardingRequest):
    try:
        return workflow.execute(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/audit")
def audit():
    return workflow.audit()

