import pytest

try:
    from scipy_doctest.conftest import dt_config
    HAVE_SCPDT = True
except ModuleNotFoundError:
    HAVE_SCPDT = False


def pytest_configure(config):
    config.addinivalue_line("markers",
                            "slow: Tests that are slow.")

