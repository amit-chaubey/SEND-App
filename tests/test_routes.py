import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Test that health check endpoint returns 200"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_words_by_sound_endpoint(client):
    """Test that words-by-sound endpoint returns fallback words"""
    response = client.get('/api/words-by-sound?sound=th')
    assert response.status_code == 200
    assert 'words' in response.json
    assert len(response.json['words']) > 0 