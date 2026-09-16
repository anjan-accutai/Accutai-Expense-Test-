from pytest_bdd import scenario


@scenario(
    "features/analytics_timeframes.feature",
    "Switch between monthly quarterly and yearly analytics",
)
def test_analytics_timeframes():
    pass