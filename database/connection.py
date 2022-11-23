from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


PATH = "/home/solarbot/images/"
DB_NAME ="images.db"

create_folder(PATH)

engine = create_engine(f"sqlite:///{os.path.join(PATH, DB_NAME)}")

Session = sessionmaker(bind=engine)

Base = declarative_base()