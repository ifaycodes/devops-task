import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['version'] == '1.0.0'


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert data['count'] == 0


def test_create_task(client):
    response = client.post('/tasks',
                           json={'title': 'Test Task'},
                           content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['completed'] == False


def test_create_task_missing_title(client):
    response = client.post('/tasks',
                           json={},
                           content_type='application/json')
    assert response.status_code == 400


def test_get_specific_task(client):
    # Create a task first
    client.post('/tasks', json={'title': 'Find Me'})

    # Get the task
    response = client.get('/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Find Me'


def test_get_nonexistent_task(client):
    response = client.get('/tasks/999')
    assert response.status_code == 404