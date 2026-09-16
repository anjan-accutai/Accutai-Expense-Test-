from pytest_bdd import scenario


@scenario(
    "features/company_budget_breakdown.feature",
    "Review company budget utilization and category breakdown",
)
def test_company_budget_breakdown():
    pass