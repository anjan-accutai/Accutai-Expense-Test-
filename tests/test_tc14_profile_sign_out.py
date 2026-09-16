from pytest_bdd import scenario


@scenario(
    "features/profile_sign_out.feature",
    "Verify profile details and sign out",
)
def test_profile_details_and_secure_sign_out():
    pass