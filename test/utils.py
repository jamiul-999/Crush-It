from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
import pytest
from models import Tocrush, Users

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:jk#*943p2k@localhost/testTocrushApplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'jhdtest', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_user():
    user = Users(
        username='jhdtest',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        hashed_password='fakehashedpassword',
        is_active=True,
        role='admin'
    )
    
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id  # Store the ID before closing
    db.close()
    
    yield user
    
    # Cleanup - delete tocrush first (foreign key), then users
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM tocrush;"))
        connection.execute(text("DELETE FROM users;"))
        connection.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
        connection.commit()

@pytest.fixture
def test_tocrush(test_user):
    tocrush = Tocrush(
        title="Solve leetcode",
        description="Do it everyday!",
        priority=5,
        complete=False,
        owner_id=test_user.id,
    )
    
    db = TestingSessionLocal()
    db.add(tocrush)
    db.commit()
    db.refresh(tocrush)
    db.close()
    
    yield tocrush
    
    # Cleanup is now handled in test_user fixture