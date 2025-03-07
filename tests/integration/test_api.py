import json
import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            pass  # Add any setup logic here if needed
        yield client

def test_shorten_url_success(client):
    """Test successful URL shortening"""
    response = client.post('/shorten', 
                         data=json.dumps({'original_url': 'https://example.com'}),
                         content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert 'short_code' in data
    assert data['original_url'] == 'https://example.com'

def test_redirect_to_original(client):
    """Test redirect to original URL"""
    # First create a short URL
    post_response = client.post('/shorten',
                              data=json.dumps({'original_url': 'https://example.com'}),
                              content_type='application/json')
    short_code = json.loads(post_response.data)['short_code']
    
    # Test redirect
    get_response = client.get(f'/{short_code}')
    
    assert get_response.status_code == 302
    assert get_response.location == 'https://example.com'

def test_shorten_invalid_url(client):
    """Test invalid URL submission"""
    response = client.post('/shorten',
                         data=json.dumps({'original_url': 'not-a-url'}),
                         content_type='application/json')
    
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

def test_nonexistent_short_code(client):
    """Test request for nonexistent short code"""
    response = client.get('/nonexistent')
    
    assert response.status_code == 404
    assert 'error' in json.loads(response.data)