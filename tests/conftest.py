import pytest
from loguru import logger


@pytest.fixture(autouse=True)
def disable_loguru_in_tests(monkeypatch):
    """Fixture to disable loguru globally during tests."""
    logger.disable("")
    monkeypatch.setattr("loguru.logger.remove", lambda *args, **kwargs: None)
    monkeypatch.setattr("loguru.logger.add", lambda *args, **kwargs: 0)
    yield
    logger.enable("")  # Re-enable loguru after the test is done
