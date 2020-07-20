from flask import Flask
import pytest

from .. import current_user
from .test_jwt import UNSIGNED_TOKEN


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    app.config['HCG_UTILS_AUTHENTICATION_JWT_VERIFY'] = False
    return app

@pytest.fixture
def client(flask_app):
    with flask_app.test_client() as client:
        yield client


def test_no_header(flask_app):
    with flask_app.test_request_context():
        assert current_user.authenticated is False


def test_garbled_header(flask_app):
    headers = {
        'x-hcx-auth-jwt-assertion': 'a random incorrect header',
    }
    with flask_app.test_request_context(headers=headers):
        assert current_user.authenticated is False


def test_current_user(flask_app):
    headers = {
        'x-hcx-auth-jwt-assertion': UNSIGNED_TOKEN,
    }
    with flask_app.test_request_context(headers=headers):
        assert current_user.authenticated is True
        assert current_user.identifier == 'logan@hcgfunds.com'
        assert current_user.first_name == 'Test'
        assert current_user.last_name == 'User'
        assert current_user.check('lcx', 'access') is True
        assert current_user.check('mcp', 'access') is False
