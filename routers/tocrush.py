from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Tocrush
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]     

class TocrushRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 
        
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Tocrush).all()

@router.get("/tocrush/{tocrush_id}", status_code=status.HTTP_200_OK)
async def read_tocrush(db: db_dependency, tocrush_id: int = Path(gt=0)):
    tocrush_model = db.query(Tocrush).filter(Tocrush.id == tocrush_id).first()
    if tocrush_model is not None:
        return tocrush_model
    raise HTTPException(status_code=404, detail="Task not found!")

@router.post("/tocrush/", status_code=status.HTTP_201_CREATED)
async def create_task(db: db_dependency, tocrush_request: TocrushRequest):
    tocrush_model = Tocrush(**tocrush_request.model_dump())
    db.add(tocrush_model)
    db.commit()
    
@router.put("/tocrush/{tocrush_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_tocrush(db: db_dependency, 
                         tocrush_request: TocrushRequest,
                         tocrush_id: int = Path(gt=0),                          
                        ):
    tocrush_model = db.query(Tocrush).filter(Tocrush.id == tocrush_id).first()
    if tocrush_model is None:
        raise HTTPException(satus_code=404, detail="Task not found!")
    
    tocrush_model.title = tocrush_request.title
    tocrush_model.description = tocrush_request.description
    tocrush_model.priority = tocrush_request.priority
    tocrush_model.complete = tocrush_request.complete
    
    db.add(tocrush_model)
    db.commit()
    
@router.delete("/tocrush/{tocrush_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tocrush(db: db_dependency, tocrush_id: int = Path(gt=0)):
    tocrush_model = db.query(Tocrush).filter(Tocrush.id == tocrush_id).first()
    if tocrush_model is None:
        raise HTTPException(status_code=404, detail="Task not found!")
    db.query(Tocrush).filter(Tocrush.id == tocrush_id).delete()
    db.commit()