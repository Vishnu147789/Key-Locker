import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from flask import session


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_register_login(client):
    # Test registration page loads
    rv = client.get('/register')
    assert rv.status_code == 200

    # Register a new user
    rv = client.post('/register', data={
        'username': 'testuser',
        'password': 'TestPass1!',
        'confirm_password': 'TestPass1!'
    }, follow_redirects=True)
    assert b'Registration successful' in rv.data

    # Test login page loads
    rv = client.get('/login')
    assert rv.status_code == 200

    # Login with new user
    rv = client.post('/login', data={
        'username': 'testuser',
        'password': 'TestPass1!'
    }, follow_redirects=True)
    assert b'dashboard' in rv.data.lower()

    # Logout
    rv = client.get('/logout', follow_redirects=True)
    assert b'logged out' in rv.data.lower()
