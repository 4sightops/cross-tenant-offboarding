from __future__ import annotations

from .models import AuditEvent, DiscoveryReport, OffboardingReport, OffboardingRequest
from .providers import MockTenantProvider


class OffboardingWorkflow:
    def __init__(self, providers: list[MockTenantProvider]) -> None:
        self.providers = providers
        self.audit_events: list[AuditEvent] = []

    def discover(self, subject: str) -> DiscoveryReport:
        accounts = []
        for provider in self.providers:
            accounts.extend(provider.discover(subject))
        self.audit_events.append(
            AuditEvent(event_type="discovery", subject=subject, detail=f"Found {len(accounts)} account(s).")
        )
        return DiscoveryReport(subject=subject, accounts=accounts)

    def execute(self, request: OffboardingRequest) -> OffboardingReport:
        expected = f"OFFBOARD {request.subject}"
        if request.confirmation != expected:
            self.audit_events.append(
                AuditEvent(event_type="confirmation_failed", subject=request.subject, detail="Typed confirmation mismatch.")
            )
            raise ValueError(f"Confirmation must exactly match: {expected}")

        discovery = self.discover(request.subject)
        actions = []
        for account in discovery.accounts:
            provider = self._provider_for(account.provider, account.tenant)
            actions.extend(provider.plan_actions(account, request.dry_run))

        summary = self._summary(request.subject, len(discovery.accounts), len(actions), request.dry_run)
        self.audit_events.append(
            AuditEvent(event_type="execution", subject=request.subject, detail=summary)
        )
        return OffboardingReport(
            subject=request.subject,
            dry_run=request.dry_run,
            account_count=len(discovery.accounts),
            actions=actions,
            technician_summary=summary,
        )

    def audit(self) -> list[AuditEvent]:
        return list(self.audit_events)

    def _provider_for(self, provider_name: str, tenant: str) -> MockTenantProvider:
        for provider in self.providers:
            if provider.provider == provider_name and provider.tenant == tenant:
                return provider
        raise ValueError(f"No provider configured for {tenant}/{provider_name}")

    @staticmethod
    def _summary(subject: str, account_count: int, action_count: int, dry_run: bool) -> str:
        mode = "Dry run" if dry_run else "Execution"
        return f"{mode} for {subject}: {account_count} account(s), {action_count} action(s)."

