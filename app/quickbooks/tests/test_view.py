import os 
import pytest
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock
from flask.testing import FlaskClient
from flask import url_for, Response, current_app, redirect, render_template, Flask
from models.quickbooks_position import QuickbooksPosition
from quickbooks.views import SavePosition
 
def test_save_quickbook_position_200(client: FlaskClient, app):
    position = QuickbooksPosition('dummy','02-02-2020','02-02-2020',12,10)
    mock_headers = {'x-hcx-auth-jwt-assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpc3MiOiJIQ1gtSUFQIiwiY29tLmhjZ2Z1bmRzLmhjeC91c2VyIjp7Imxhc3RfbmFtZSI6IlVzZXIiLCJmaXJzdF9uYW1lIjoiVGVzdCIsInJvbGVzIjpbWyJoZWFkZXItZWNobyIsImFjY2VzcyJdLFsiaGVhZGVyLWVjaG8iLCJ1cGRhdGUiXV0sImlkZW50aWZpZXIiOiJyb21hbkBleGFtcGxlLmNvbSJ9LCJpYXQiOjE1OTQxNDIwOTQsImNvbS5oY2dmdW5kcy5oY3gvYWN0aW9uIjoiYWNjZXNzIiwiYXVkIjoiaGVhZGVyLWVjaG8iLCJleHAiOjQwNzA5MDg4MDAsIm5iZiI6MTU5NDE0MjA5NCwic3ViIjoicm9tYW5AZXhhbXBsZS5jb20ifQ.' }
    data = {
        "as_of_date": datetime.utcnow(),
        "period" : "2020-07-11",
        "wisetack_junior_position" : 12.12,
        "lighter_junior_position" : 15
    }  
    with app.app_context():
        url = url_for('quickbooks.save_position')
        response = client.post(url,data=data,headers=mock_headers)
        assert response.status_code == 200
        assert "localhost/save_position" in url


def test_no_wisetack_junior_(client: FlaskClient, app):
    data = {
        "submitter" : "dummy",
        "as_of_date": datetime.utcnow(),
        "period" : "2020-07-11",
        "lighter_junior_position" : 15
    }  
    with app.app_context():
        url = url_for('quickbooks.save_position')
        template = render_template('quickbooks/success-page.html')
    response = client.post(url,data=data)
    assert response.status_code == 400
    assert response.data.decode() != template

def test_no_lighter_junior_position(client: FlaskClient, app):
    data = {
        "submitter" : "dummy",
        "as_of_date": datetime.utcnow(),
        "period" : "2020-07-11",
        "wisetack_junior_position" : 154.5
    }  
    with app.app_context():
        url = url_for('quickbooks.save_position')
        template = render_template('quickbooks/success-page.html')
    response = client.post(url,data=data)
    assert response.status_code == 400
    assert response.data.decode() != template

def test_get_form_quickbook_status_200(client: FlaskClient, app):
    with app.app_context():
        url = url_for('quickbooks.form_quickbook')
    response = client.get(url)
    assert response.status_code == 200


