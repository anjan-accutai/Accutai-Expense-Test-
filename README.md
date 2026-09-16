# Accutai Playwright Tests

This project uses Playwright, pytest, and pytest-bdd to test the Accutai Financial Portal. Each executable test case is connected to a Gherkin feature under `tests/features/`.

## Run Tests

Run all collected scenarios with a visible Chromium browser:

```powershell
uv run pytest tests/ --headed -v
```

Generate the self-contained HTML report:

```powershell
uv run pytest tests/ --headed -v --html=reports/test-report.html --self-contained-html --css=reports/dark-theme.css
```

Run one test case:

```powershell
uv run pytest tests/test_tc14_profile_sign_out.py --headed -v
```

## Test Coverage

The current suite contains 14 active scenarios:

- TC01: Launch portal
- TC02: Valid user login
- TC05: New-user signup
- TC08: Dashboard budget metrics
- TC09: Sidebar navigation
- TC10: Transaction creation
- TC11: Transaction search and filtering
- TC12: Receipt viewing
- TC14: Profile details and secure sign out
- TC17: View All in Ledger shortcut
- TC18: Shared Ledger audit view
- TC19: Future-dated expense entry
- TC20: Company Budget breakdown
- TC21: Analytics timeframe toggles

Defect-marked cases were removed from active execution: TC03, TC04, TC06, TC07, TC13, TC15, TC16, and TC22.

## Clear Transactions

Delete all transactions across the supported month and year filters:

```powershell
uv run python scripts/delete_all_transactions.py
```

The cleanup script logs in with `ACCUTAI_USERNAME` and `ACCUTAI_PASSWORD` when those environment variables are set; otherwise it uses the repository defaults.

## Structure

- `tests/features/`: Gherkin scenarios for the active test cases
- `tests/steps.py`: Shared pytest-bdd step definitions
- `tests/test_tc*.py`: Test-case entry points
- `conftest.py`: Shared pytest fixtures
- `pytest.ini`: Base URL and test discovery configuration
- `reports/test-report.html`: Generated test report
- `reports/dark-theme.css`: Dark theme applied to generated reports
