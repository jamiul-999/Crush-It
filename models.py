from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Tocrush(Base):
    __tablename__ = 'tocrush'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Boolean, default=False)