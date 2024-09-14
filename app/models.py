from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# tabella 'sites'
class Site(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    long = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    id_meteo = Column(Integer, ForeignKey('meteo_info.id'))

    # Relazione con la tabella meteo_info
    meteo_info = relationship('MeteoInfo', back_populates='sites')

# tabella 'meteo_info'
class MeteoInfo(Base):
    __tablename__ = 'meteo_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    temperature_2m = Column(Float, nullable=False)
    relative_humidity_2m = Column(Float, nullable=False)
    dew_point_2m = Column(Float, nullable=False)
    pressure_msl = Column(Float, nullable=False)
    surface_pressure = Column(Float, nullable=False)

    # Relazione con la tabella sites
    sites = relationship('Site', back_populates='meteo_info')

