import pytest
from app.application import Application


@pytest.fixture
def app():
    appl = Application()
    yield appl
    appl.quit()
