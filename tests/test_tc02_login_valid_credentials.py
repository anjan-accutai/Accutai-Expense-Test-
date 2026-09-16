from pytest_bdd import scenario


@scenario("features/login_valid.feature", "Login with valid credentials")
def test_existing_user_login_valid_credentials():
    pass
