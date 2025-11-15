from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Tocrush
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
     prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]   
user_dependency = Annotated[dict, Depends(get_current_user)]  



@router.get("/tocrush", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authenticationo Failed')
    return db.query(Tocrush).all()

@router.delete("/tocrush/{tocrush_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tocrush(user: user_dependency,
                         db: db_dependency,
                         tocrush_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Tocrush).filter(Tocrush.id == tocrush_id).first()
    if tocrush_model is None:
        raise HTTPException(status_code=404, detail="Task not found!!")
    db.query(Tocrush).filter(Tocrush.id == tocrush_id).delete()
    db.commit()