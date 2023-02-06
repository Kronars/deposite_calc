import pytest
from flask import Flask

from flaskr import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture()
def client(app: Flask):
    return app.test_client()
