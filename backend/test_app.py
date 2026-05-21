import pytest
from app import app, init_db

# ── this fixture is required by all tests ──
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

# ── validation tests ──
def test_missing_type_returens_400(client):
    response = client.post('/transactions', json= {
        'amount': 50.0,
        'category': 'food'
    })
    assert response.status_code == 400
    
def test_invalid_type_returns_400(client):
    response = client.post('/transactions', json= {
        'type': 'pizza',
        'amount': 50.0,
        'category': 'food'
    })
    assert response.status_code == 400
    
def test_negative_amount_returns_400(client):
    response = client.post('/transactions', json= {
        'type': 'expense',
        'amount': -50.0,
        'category':'food'
    })
    assert response.status_code == 400
    
def test_delete_nonexitent_returns_404(client):
    response = client.delete('/transactions/9999')
    assert response.status_code == 404