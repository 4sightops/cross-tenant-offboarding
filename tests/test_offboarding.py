import pytest
from cross_tenant_offboarding.models import OffboardingRequest
from cross_tenant_offboarding.providers import demo_providers
from cross_tenant_offboarding.workflow import OffboardingWorkflow


def test_discovery_returns_all_mock_tenants():
    workflow = OffboardingWorkflow(demo_providers())
    result = workflow.discover("TestUserOne")
    assert len(result.accounts) == 2
    assert {account.tenant for account in result.accounts} == {"DemoTenant", "ExampleCo"}


def test_confirmation_must_match_subject():
    workflow = OffboardingWorkflow(demo_providers())
    with pytest.raises(ValueError):
        workflow.execute(OffboardingRequest(subject="TestUserOne", confirmation="OFFBOARD TestUserTwo"))


def test_dry_run_execution_records_safe_actions():
    workflow = OffboardingWorkflow(demo_providers())
    report = workflow.execute(
        OffboardingRequest(subject="TestUserOne", confirmation="OFFBOARD TestUserOne", dry_run=True)
    )
    assert report.dry_run is True
    assert report.account_count == 2
    assert len(report.actions) == 8
    assert {action.status for action in report.actions} == {"dry_run"}
    assert workflow.audit()[-1].event_type == "execution"

