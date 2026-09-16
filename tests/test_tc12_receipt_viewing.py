from pytest_bdd import scenario


@scenario(
    "features/receipt_viewing.feature",
    "View an attached receipt from a transaction",
)
def test_receipt_viewing():
    pass