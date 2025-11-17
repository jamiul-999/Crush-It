from .utils import *
from routers.admin import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_tocrush):
    response = client.get("/admin/tocrush")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Solve leetcode',
                                'description': 'Do it everyday!', 'id': test_tocrush.id,
                                'priority': 5, 'owner_id': test_tocrush.owner_id}]