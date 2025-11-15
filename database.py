from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


POSTGRESQL_DATABASE_URL = 'postgresql://postgres:jk#*943p2k@localhost/TocrushApplicationDatabase'

engine = create_engine(POSTGRESQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()