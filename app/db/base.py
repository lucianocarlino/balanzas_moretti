from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
conn = engine.connect()
Base = declarative_base()
Meta = MetaData()

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)