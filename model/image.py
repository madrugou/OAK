from sqlalchemy import Column, Integer, String, Float, DateTime
from database.connection import Base, engine
from sqlalchemy.sql import func


class Image(Base):
    __tablename__ = 'tb_image'
    cd_image = Column("code", Integer,  primary_key=True, autoincrement=True)
    name =  Column("name", String)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)
    dt_created = Column("dt_created", DateTime)


    def __init__(self, name, latitude, longitude):
        self.name = name 
        self.latitude = latitude
        self.longitude = longitude
        self.dt_created = func.now()


Image.metadata.create_all(engine)