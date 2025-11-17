from .utils import *
from routers.admin import get_db, get_current_user
from fastapi import status
from models import Tocrush

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_tocrush):
    response = client.get("/admin/tocrush")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Solve leetcode',
                                'description': 'Do it everyday!', 'id': test_tocrush.id,
                                'priority': 5, 'owner_id': test_tocrush.owner_id}]
    
def test_admin_delete_tocrush(test_tocrush):
    response = client.delete(f'/admin/tocrush/{test_tocrush.id}')
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Tocrush).filter(Tocrush.id == test_tocrush.id).first()
    assert model is None
    
def test_admin_delete_tocrush_not_found():
    response = client.delete("/admin/tocrush/9999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found!!'}