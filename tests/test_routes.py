import pytest
from app import create_app, db
from app.models import User, Word

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_root_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Spelling App API!"}

def test_register_user(client):
    response = client.post('/user/', json={"username": "test_user"})
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully."

    # Check duplicate username
    response = client.post('/user/', json={"username": "test_user"})
    assert response.status_code == 409
    assert response.json['error'] == "Username already exists."

def test_fetch_word(client):
    response = client.post('/word/', json={"focus_sound": "ph", "difficulty_level": 2})
    assert response.status_code == 200
    assert 'word' in response.json
    assert response.json['difficulty_level'] == 2

def test_submit_score(client):
    # Register a user and create a word for testing
    client.post('/user/', json={"username": "test_user"})
    word = Word(word="phone", focus_sound="ph", difficulty_level=2)
    db.session.add(word)
    db.session.commit()

    # Submit a score
    response = client.post('/score/', json={"user_id": 1, "word_id": 1, "score": 85})
    assert response.status_code == 200
    assert response.json['message'] == "Score submitted successfully."
