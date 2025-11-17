from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ['username'] == 'jhdtest'
    assert response.json()['email'] == 'test@example.com'
    assert response.json()['first_name'] == 'Test'
    assert response.json()['last_name'] == 'User'
    assert response.json()['is_active'] == True
    assert response.json()['role'] == 'admin'
    
def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "fakehashedpassword",
                                                  "new_password":"newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wronghashedpassword",
                                                  "new_password":"newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication failed'}