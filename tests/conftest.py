import pytest
from flask import Flask

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app
 
@pytest.fixture
def client(app: Flask):
    with app.test_client() as client:
        yield client
