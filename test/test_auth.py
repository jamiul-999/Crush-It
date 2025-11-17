from .utils import *
from routers.auth import get_db, authenticate_user

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'fakehashedpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username