from fastapi import FastAPI
import models
from database import engine
from routers import auth, tocrush, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(tocrush.router)
app.include_router(admin.router)
app.include_router(users.router)