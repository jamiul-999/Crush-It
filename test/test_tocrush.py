from routers.tocrush import get_db, get_current_user
from fastapi import status
from models import Tocrush, Users
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_tocrush):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    
    expected_data = [{
        'complete': False,
        'title': 'Solve leetcode',
        'description': 'Do it everyday!',
        'id': test_tocrush.id,
        'priority': 5,
        'owner_id': test_tocrush.owner_id
    }]
    
    assert response.json() == expected_data
    
def test_read_one_authenticated(test_tocrush):
    response = client.get(f"/tocrush/{test_tocrush.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'complete': False,
        'title': 'Solve leetcode',
        'description': 'Do it everyday!',
        'id': test_tocrush.id,
        'priority': 5,
        'owner_id': test_tocrush.owner_id
    }
    
def test_read_one_authenticated_not_found():
    response = client.get("/tocrush/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found!'}
    
def test_create_tocrush(test_tocrush):
    request_data={
        'title': 'New task!',
        'description': 'New task description',
        'priority': 5,
        'complete': False,
    }
    
    response = client.post('/tocrush/', json=request_data)
    assert response.status_code == 201
    
    db = TestingSessionLocal()
    model = db.query(Tocrush).filter(Tocrush.title == request_data['title']).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
def test_update_tocrush(test_tocrush):
    request_data={
        'title': 'Change the title of the tocrush already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }
    
    response = client.put(f'/tocrush/{test_tocrush.id}', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Tocrush).filter(Tocrush.id == test_tocrush.id).first()
    assert model.title == 'Change the title of the tocrush already saved!'
    
def test_update_tocrush_not_found(test_tocrush):
    request_data={
        'title': 'Change the title of the tocrush already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }
    
    response = client.put('/tocrush/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found!'}
    
def test_delete_tocrush(test_tocrush):
    response = client.delete(f'/tocrush/{test_tocrush.id}')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Tocrush).filter(Tocrush.id == test_tocrush.id).first()
    assert model is None
    
def test_delete_tocrush_not_found(test_tocrush):
    response = client.delete('/tocrush/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found!'}