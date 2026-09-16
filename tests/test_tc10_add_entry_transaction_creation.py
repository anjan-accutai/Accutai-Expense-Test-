from pytest_bdd import scenario


@scenario(
    "features/add_entry_transaction_creation.feature",
    "Record a transaction for each category",
)
def test_add_entry_transaction_creation():
    pass
