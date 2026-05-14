from __future__ import annotations

from copy import deepcopy
from .models import AccountRecord, ActionRecord


class RedactedTenantProvider:
    def __init__(self, provider: str, tenant: str, accounts: list[AccountRecord]) -> None:
        self.provider = provider
        self.tenant = tenant
        self._accounts = accounts

    def discover(self, subject: str) -> list[AccountRecord]:
        return [deepcopy(account) for account in self._accounts if account.subject.lower() == subject.lower()]

    def plan_actions(self, account: AccountRecord, dry_run: bool) -> list[ActionRecord]:
        status = "dry_run" if dry_run else "succeeded"
        prefix = "Would" if dry_run else "Did"
        if account.provider == "okta":
            return [
                ActionRecord(
                    tenant=account.tenant,
                    provider=account.provider,
                    action="suspend_user",
                    status=status,
                    detail=f"{prefix} suspend SaaS identity account for {account.subject}.",
                ),
                ActionRecord(
                    tenant=account.tenant,
                    provider=account.provider,
                    action="clear_sessions",
                    status=status,
                    detail=f"{prefix} clear active SaaS sessions.",
                ),
                ActionRecord(
                    tenant=account.tenant,
                    provider=account.provider,
                    action="remove_application_groups",
                    status=status,
                    detail=f"{prefix} remove {len(account.groups)} SaaS group membership(s).",
                ),
            ]
        return [
            ActionRecord(
                tenant=account.tenant,
                provider=account.provider,
                action="disable_sign_in",
                status=status,
                detail=f"{prefix} disable sign-in for {account.subject}.",
            ),
            ActionRecord(
                tenant=account.tenant,
                provider=account.provider,
                action="revoke_sessions",
                status=status,
                detail=f"{prefix} revoke active sessions.",
            ),
            ActionRecord(
                tenant=account.tenant,
                provider=account.provider,
                action="convert_mailbox_to_shared",
                status=status,
                detail=f"{prefix} convert Exchange Online mailbox to shared before license removal.",
            ),
            ActionRecord(
                tenant=account.tenant,
                provider=account.provider,
                action="remove_group_memberships",
                status=status,
                detail=f"{prefix} remove {len(account.groups)} group membership(s).",
            ),
            ActionRecord(
                tenant=account.tenant,
                provider=account.provider,
                action="remove_license_assignments",
                status=status,
                detail=f"{prefix} remove {len(account.licenses)} license assignment(s).",
            ),
        ]


def configured_providers() -> list[RedactedTenantProvider]:
    return [
        RedactedTenantProvider(
            provider="microsoft-graph",
            tenant="RedactedTenant",
            accounts=[
                AccountRecord(
                    subject="TestUserOne",
                    tenant="RedactedTenant",
                    provider="microsoft-graph",
                    enabled=True,
                    groups=["Service Desk Readers", "Project Members"],
                    licenses=["Productivity Seat"],
                )
            ],
        ),
        RedactedTenantProvider(
            provider="okta",
            tenant="ExampleCo",
            accounts=[
                AccountRecord(
                    subject="TestUserOne",
                    tenant="ExampleCo",
                    provider="okta",
                    enabled=True,
                    groups=["Operations"],
                    licenses=["Standard Seat"],
                )
            ],
        ),
    ]
