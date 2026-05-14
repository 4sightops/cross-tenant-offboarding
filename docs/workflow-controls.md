# Workflow Controls

This is a clean-room educational/demo implementation inspired by common enterprise automation patterns. It does not contain proprietary code, data, credentials, or confidential business logic from any employer or client.

## Production-Style Sequence

1. Discover the subject in Microsoft Graph-managed tenants and SaaS identity providers.
2. Revalidate the selected accounts before execution.
3. Require exact typed confirmation.
4. Convert or preserve Exchange Online mailbox state before license removal.
5. Revoke sessions and remove risky access.
6. Remove group memberships and license assignments.
7. Write an audit event and a technician-facing summary.

## Why Mailbox Preservation Is Separate

Offboarding automation should not remove licenses before the mailbox disposition is known. The demo models mailbox conversion as its own action so tests can verify that the planned workflow preserves mailbox access before license cleanup.

## What Is Intentionally Omitted

- Real production identifiers
- Real user principal names
- Real ticket numbers
- Real mailbox addresses
- Real Graph, Exchange Online, Okta, or ServiceNow clients
