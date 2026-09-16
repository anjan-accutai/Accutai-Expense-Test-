from pytest_bdd import scenario


@scenario("features/future_expense.feature", "Record a future dated expense")
def test_future_expense():
    pass