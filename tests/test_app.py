import sys
import os
import pytest

# Add the project root to sys.path so 'app' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Now import 'app' after modifying sys.path


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_delete_key(client):
    # Login first
    login_response = client.post('/login', data={
        'username': 'testuser',
        'password': 'TestPass1!'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    # Add a key
    add_key_response = client.post('/add_key', data={
        'key_name': 'api_key',
        'key_value': '123456',
        'key_description': 'API key for service'
    }, follow_redirects=True)
    assert b'Key added successfully' in add_key_response.data

    # Delete the key
    delete_key_response = client.get('/delete_key/api_key', follow_redirects=True)
    assert b'Key deleted successfully' in delete_key_response.data
