import pytest
from playwright.sync_api import expect

pytest_plugins = ["tests.steps"]


@pytest.fixture(scope="session")
def valid_credentials():
    return {"username": "anjan", "password": "123456"}


@pytest.fixture
def authenticated_page(page, valid_credentials):
    page.goto("/")
    page.get_by_placeholder("demo@accutai.com or username").fill(
        valid_credentials["username"]
    )
    page.get_by_placeholder("••••••••").fill(valid_credentials["password"])
    page.get_by_role("button", name="Access Shared Ledger").click()
    expect(page.get_by_role("button", name="Sign Out")).to_be_visible(timeout=30000)
    return page