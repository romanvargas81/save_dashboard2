import os
import json
from shutil import copyfile
import pytest
from faker import Faker
from pytest_mock import MockFixture
from flask import testing
from werkzeug.datastructures import Headers
from flask import current_app

from app import app as base_app
from quickbooks.views import QUIKBOOKS

faker = Faker()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def app(app_config):
    base_app.config.update(app_config)
    return base_app

class TestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        api_key_headers = Headers({
            'x-hcx-auth-jwt-assertion': '123'
        })
        headers = kwargs.pop('headers', Headers())
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)

@pytest.fixture(scope="session")
def app_config(DB_URI):
    return {
        "HASHING_KEY": str.encode(faker.name()),
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost",
        "DB_URI": DB_URI  
    }

@pytest.fixture(scope="session")
def DB_URI():
    return os.environ['DB_URI']

    