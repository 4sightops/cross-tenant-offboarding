from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel


class AccountRecord(BaseModel):
    subject: str
    tenant: str
    provider: str
    enabled: bool
    groups: list[str]
    licenses: list[str]


class DiscoveryReport(BaseModel):
    subject: str
    accounts: list[AccountRecord]


class OffboardingRequest(BaseModel):
    subject: str
    confirmation: str
    dry_run: bool = True


class ActionRecord(BaseModel):
    tenant: str
    provider: str
    action: str
    status: str
    detail: str


class OffboardingReport(BaseModel):
    subject: str
    dry_run: bool
    account_count: int
    actions: list[ActionRecord]
    technician_summary: str


class AuditEvent(BaseModel):
    event_type: str
    subject: str
    detail: str
    actor: str = "DemoOperator"
    created_at: datetime = datetime.now(timezone.utc)

