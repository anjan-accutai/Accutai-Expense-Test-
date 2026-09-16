from pytest_bdd import scenario


@scenario("features/signup_new_user.feature", "Create a new user account")
def test_new_user_signup():
    pass