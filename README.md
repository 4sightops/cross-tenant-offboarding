# Cross-Tenant Offboarding

This is a clean-room educational/demo implementation inspired by common enterprise automation patterns. It does not contain proprietary code, data, credentials, or confidential business logic from any employer or client.

Cross-Tenant Offboarding demonstrates a safety-first identity lifecycle workflow across synthetic tenants. It uses mock providers and fake accounts to model discovery, review, confirmation, dry-run execution, and audit evidence without contacting real directories, ticketing systems, mail systems, or customer environments.

## Architecture

```mermaid
flowchart TD
    Operator["Demo operator"] --> API["FastAPI app"]
    API --> Workflow["Offboarding workflow"]
    Workflow --> ProviderA["DemoTenant provider"]
    Workflow --> ProviderB["ExampleCo provider"]
    Workflow --> Gate["Typed confirmation gate"]
    Workflow --> Audit["Append-only audit trail"]
    Workflow --> Report["Markdown-style execution summary"]
```

## Demo Workflow

1. Discover a user across configured mock tenants.
2. Review account status, group memberships, and license labels.
3. Require exact typed confirmation before execution.
4. Execute in dry-run mode by default.
5. Record an audit event for discovery, confirmation failures, and execution.
6. Return a technician-readable summary of planned actions.

## Safety Controls

- No live API clients are included.
- No production identifiers are included.
- No real users, domains, tickets, groups, devices, or logs are included.
- Execution defaults to dry run.
- Confirmation must exactly match `OFFBOARD <subject>`.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn cross_tenant_offboarding.app:app --reload --port 8040
```

Open the local API docs path shown by the dev server.

## Demo Endpoints

| Route | Purpose |
|---|---|
| `GET /subjects/{subject}/discover` | Discover mock accounts |
| `POST /offboarding/execute` | Run confirmed dry-run offboarding |
| `GET /audit` | View audit events |
