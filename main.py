from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, status
import models
from models import Tocrush
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]        
        
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Tocrush).all()

@app.get("/tocrush/{tocrush_id}", status_code=status.HTTP_200_OK)
async def read_tocrush(db: db_dependency, tocrush_id: int = Path(gt=0)):
    tocrush_model = db.query(Tocrush).filter(Tocrush.id == tocrush_id).first()
    if tocrush_model is not None:
        return tocrush_model
    raise HTTPException(status_code=404, detail="Task not found!")